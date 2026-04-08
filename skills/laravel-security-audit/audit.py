#!/usr/bin/env python3
"""
Laravel Security Audit Script
Automatisierte Prüfung der häufigsten Sicherheitsprobleme in Laravel-Applikationen.
"""

import json
import os
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime


class Finding:
    def __init__(self, severity, category, title, description, file=None, line=None, recommendation=None):
        self.severity = severity  # critical, high, medium, low
        self.category = category
        self.title = title
        self.description = description
        self.file = file
        self.line = line
        self.recommendation = recommendation

    def to_dict(self):
        d = {
            "severity": self.severity,
            "category": self.category,
            "title": self.title,
            "description": self.description,
        }
        if self.file:
            d["file"] = self.file
        if self.line:
            d["line"] = self.line
        if self.recommendation:
            d["recommendation"] = self.recommendation
        return d


class LaravelSecurityAudit:
    def __init__(self, project_path):
        self.project_path = Path(project_path).resolve()
        self.findings = []
        self.info = {}

    def run(self):
        """Run all audit checks."""
        print(f"🔍 Starting Laravel Security Audit: {self.project_path}")
        print("=" * 60)

        if not self._verify_laravel_project():
            return self._output_results()

        self._collect_project_info()
        self._check_env_config()
        self._check_debug_mode()
        self._check_app_key()
        self._check_session_config()
        self._check_csrf_exceptions()
        self._check_cors_config()
        self._check_raw_queries()
        self._check_unescaped_blade()
        self._check_mass_assignment()
        self._check_env_calls_in_app()
        self._check_debug_statements()
        self._check_file_permissions()
        self._check_https_enforcement()
        self._check_rate_limiting()
        self._check_unprotected_routes()
        self._check_external_resources()
        self._check_composer_audit()
        self._check_storage_links()
        self._check_telescope_horizon()
        self._check_error_pages()
        self._check_log_config()
        self._check_cookie_config()
        self._check_password_config()
        self._check_trusted_proxies()
        self._check_git_secrets()

        return self._output_results()

    def _verify_laravel_project(self):
        """Verify this is a Laravel project."""
        artisan = self.project_path / "artisan"
        composer_json = self.project_path / "composer.json"

        if not artisan.exists() or not composer_json.exists():
            self.findings.append(Finding(
                "critical", "setup",
                "Kein Laravel-Projekt gefunden",
                f"Der Pfad {self.project_path} scheint kein Laravel-Projekt zu sein.",
                recommendation="Stelle sicher, dass der korrekte Projektpfad angegeben wird."
            ))
            return False
        return True

    def _collect_project_info(self):
        """Collect basic project information."""
        composer_json = self.project_path / "composer.json"
        try:
            with open(composer_json) as f:
                data = json.load(f)
                self.info["name"] = data.get("name", "unknown")
                require = data.get("require", {})
                self.info["laravel_version"] = require.get("laravel/framework", "unknown")
                self.info["php_version"] = require.get("php", "unknown")
        except Exception:
            self.info["name"] = "unknown"

        # Check PHP version
        try:
            result = subprocess.run(["php", "-v"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                match = re.search(r"PHP (\d+\.\d+\.\d+)", result.stdout)
                if match:
                    self.info["php_runtime_version"] = match.group(1)
        except Exception:
            pass

        self.info["audit_date"] = datetime.now().isoformat()

    def _read_file(self, relative_path):
        """Safely read a file relative to project root."""
        try:
            full_path = self.project_path / relative_path
            if full_path.exists():
                return full_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass
        return None

    def _search_files(self, pattern, directory, extensions=None):
        """Search for regex pattern in files."""
        results = []
        search_dir = self.project_path / directory
        if not search_dir.exists():
            return results

        for root, dirs, files in os.walk(search_dir):
            # Skip vendor, node_modules, storage
            dirs[:] = [d for d in dirs if d not in ("vendor", "node_modules", "storage", ".git")]
            for fname in files:
                if extensions and not any(fname.endswith(ext) for ext in extensions):
                    continue
                fpath = Path(root) / fname
                try:
                    content = fpath.read_text(encoding="utf-8", errors="replace")
                    for i, line in enumerate(content.splitlines(), 1):
                        if re.search(pattern, line):
                            rel = str(fpath.relative_to(self.project_path))
                            results.append({"file": rel, "line": i, "content": line.strip()})
                except Exception:
                    continue
        return results

    def _check_env_config(self):
        """Check .env file for security issues."""
        env_content = self._read_file(".env")
        env_example = self._read_file(".env.example")

        if env_content is None:
            self.findings.append(Finding(
                "high", "config",
                "Keine .env Datei gefunden",
                "Die .env Datei fehlt oder ist nicht lesbar.",
                file=".env",
                recommendation="Erstelle eine .env Datei basierend auf .env.example"
            ))
            return

        # Check APP_ENV
        match = re.search(r"^APP_ENV\s*=\s*(.+)$", env_content, re.MULTILINE)
        if match:
            value = match.group(1).strip()
            if value != "production":
                self.findings.append(Finding(
                    "high", "config",
                    f"APP_ENV ist '{value}' (nicht 'production')",
                    "Für Production muss APP_ENV=production gesetzt sein.",
                    file=".env",
                    recommendation="Setze APP_ENV=production"
                ))

        # Check APP_DEBUG
        match = re.search(r"^APP_DEBUG\s*=\s*(.+)$", env_content, re.MULTILINE)
        if match:
            value = match.group(1).strip().lower()
            if value in ("true", "1", "yes"):
                self.findings.append(Finding(
                    "critical", "config",
                    "APP_DEBUG ist aktiviert",
                    "Debug-Modus zeigt Stack Traces, Environment-Variablen und sensible Daten an.",
                    file=".env",
                    recommendation="Setze APP_DEBUG=false für Production"
                ))

        # Check for default/weak values
        weak_patterns = {
            "APP_KEY": (r"^APP_KEY\s*=\s*$", "APP_KEY ist leer"),
            "DB_PASSWORD": (r"^DB_PASSWORD\s*=\s*(password|secret|root|admin|123|)\s*$", "Schwaches DB-Passwort"),
            "MAIL_PASSWORD": (r"^MAIL_PASSWORD\s*=\s*$", "MAIL_PASSWORD ist leer"),
        }

        for key, (pattern, msg) in weak_patterns.items():
            if re.search(pattern, env_content, re.MULTILINE | re.IGNORECASE):
                self.findings.append(Finding(
                    "high", "secrets",
                    msg,
                    f"{key} hat einen unsicheren oder leeren Wert.",
                    file=".env",
                    recommendation=f"Setze einen sicheren Wert für {key}"
                ))

        # Check if .env.example contains actual secrets
        if env_example:
            secret_patterns = [
                (r"^(DB_PASSWORD|MAIL_PASSWORD|AWS_SECRET|API_KEY|APP_KEY)\s*=\s*[^${\s].{5,}", "example_secrets"),
            ]
            for pattern, _ in secret_patterns:
                matches = re.findall(pattern, env_example, re.MULTILINE)
                if matches:
                    self.findings.append(Finding(
                        "high", "secrets",
                        "Secrets in .env.example gefunden",
                        ".env.example sollte keine echten Secrets enthalten, da sie im Git-Repo landen.",
                        file=".env.example",
                        recommendation="Entferne alle echten Werte aus .env.example und verwende Platzhalter"
                    ))
                    break

    def _check_debug_mode(self):
        """Check for debug-related packages in production."""
        composer_json = self._read_file("composer.json")
        if not composer_json:
            return

        try:
            data = json.loads(composer_json)
            require = data.get("require", {})
            debug_packages = ["barryvdh/laravel-debugbar", "laravel/telescope"]
            for pkg in debug_packages:
                if pkg in require:
                    self.findings.append(Finding(
                        "high", "config",
                        f"{pkg} ist in require (nicht require-dev)",
                        f"Debug-Package {pkg} sollte nur in require-dev stehen.",
                        file="composer.json",
                        recommendation=f"Verschiebe {pkg} von 'require' nach 'require-dev'"
                    ))
        except json.JSONDecodeError:
            pass

    def _check_app_key(self):
        """Check APP_KEY configuration."""
        env = self._read_file(".env")
        if not env:
            return

        match = re.search(r"^APP_KEY\s*=\s*(.+)$", env, re.MULTILINE)
        if match:
            key = match.group(1).strip()
            if not key:
                self.findings.append(Finding(
                    "critical", "config",
                    "APP_KEY ist nicht gesetzt",
                    "Ohne APP_KEY sind verschlüsselte Daten, Sessions und Cookies unsicher.",
                    file=".env",
                    recommendation="Führe 'php artisan key:generate' aus"
                ))
            elif not key.startswith("base64:"):
                self.findings.append(Finding(
                    "medium", "config",
                    "APP_KEY ist nicht im base64-Format",
                    "Der APP_KEY sollte im base64:-Format sein.",
                    file=".env",
                    recommendation="Führe 'php artisan key:generate' aus, um einen neuen Key zu generieren"
                ))

    def _check_session_config(self):
        """Check session security configuration."""
        config = self._read_file("config/session.php")
        if not config:
            return

        checks = [
            (r"'secure'\s*=>\s*(?:env\([^)]*,\s*)?false", "medium",
             "Session Cookie nicht auf 'secure' gesetzt",
             "Session Cookies sollten nur über HTTPS gesendet werden.",
             "Setze 'secure' => true in config/session.php oder SESSION_SECURE_COOKIE=true in .env"),
            (r"'http_only'\s*=>\s*false", "high",
             "Session Cookie http_only ist deaktiviert",
             "Ohne http_only kann JavaScript auf Session Cookies zugreifen (XSS-Risiko).",
             "Setze 'http_only' => true in config/session.php"),
            (r"'same_site'\s*=>\s*(?:env\([^)]*,\s*)?['\"]?none['\"]?", "medium",
             "Session same_site ist 'none'",
             "same_site=none erlaubt Cross-Site Cookie-Nutzung.",
             "Setze same_site auf 'lax' oder 'strict'"),
        ]

        for pattern, severity, title, desc, rec in checks:
            if re.search(pattern, config, re.IGNORECASE):
                self.findings.append(Finding(severity, "session", title, desc,
                                             file="config/session.php", recommendation=rec))

        # Check session driver
        env = self._read_file(".env")
        if env:
            match = re.search(r"^SESSION_DRIVER\s*=\s*(.+)$", env, re.MULTILINE)
            if match and match.group(1).strip() == "file":
                self.findings.append(Finding(
                    "medium", "session",
                    "SESSION_DRIVER ist 'file'",
                    "File-basierte Sessions sind langsamer und schwerer zu skalieren. "
                    "Für Production wird redis oder database empfohlen.",
                    file=".env",
                    recommendation="Verwende SESSION_DRIVER=redis oder SESSION_DRIVER=database"
                ))

    def _check_csrf_exceptions(self):
        """Check for CSRF exceptions."""
        # Laravel 11+ (bootstrap/app.php)
        app_bootstrap = self._read_file("bootstrap/app.php")
        if app_bootstrap and "validateCsrfTokens" in app_bootstrap:
            excepts = re.findall(r"except:\s*\[([^\]]+)\]", app_bootstrap)
            if excepts:
                self.findings.append(Finding(
                    "high", "csrf",
                    "CSRF-Token Validierung hat Ausnahmen",
                    f"Folgende Routes sind von CSRF-Schutz ausgenommen: {excepts[0].strip()}",
                    file="bootstrap/app.php",
                    recommendation="Prüfe ob alle CSRF-Ausnahmen wirklich nötig sind (z.B. Webhook-Endpoints)"
                ))

        # Laravel 10 and below
        csrf_middleware = self._read_file("app/Http/Middleware/VerifyCsrfToken.php")
        if csrf_middleware:
            except_match = re.search(r"\$except\s*=\s*\[([^\]]*)\]", csrf_middleware, re.DOTALL)
            if except_match and except_match.group(1).strip():
                self.findings.append(Finding(
                    "high", "csrf",
                    "CSRF VerifyCsrfToken hat Ausnahmen",
                    f"Routes in $except sind nicht CSRF-geschützt.",
                    file="app/Http/Middleware/VerifyCsrfToken.php",
                    recommendation="Prüfe ob alle Einträge in $except wirklich nötig sind"
                ))

    def _check_cors_config(self):
        """Check CORS configuration."""
        cors_config = self._read_file("config/cors.php")
        if cors_config:
            if re.search(r"'allowed_origins'\s*=>\s*\[\s*'\*'\s*\]", cors_config):
                self.findings.append(Finding(
                    "medium", "cors",
                    "CORS erlaubt alle Origins (*)",
                    "Wildcard CORS erlaubt jeder Domain, Requests an die API zu senden.",
                    file="config/cors.php",
                    recommendation="Beschränke allowed_origins auf die tatsächlich benötigten Domains"
                ))

    def _check_raw_queries(self):
        """Check for potential SQL injection via raw queries."""
        patterns = [
            r"DB::raw\s*\(",
            r"->whereRaw\s*\(",
            r"->selectRaw\s*\(",
            r"->orderByRaw\s*\(",
            r"->havingRaw\s*\(",
            r"->groupByRaw\s*\(",
        ]

        for pattern in patterns:
            results = self._search_files(pattern, "app", [".php"])
            for r in results:
                # Check if bindings are used (second parameter)
                if not re.search(r",\s*\[", r["content"]):
                    self.findings.append(Finding(
                        "critical", "sql_injection",
                        f"Raw Query ohne Bindings: {pattern.split('::')[0] if '::' in pattern else pattern}",
                        f"Raw Query möglicherweise ohne Parameter-Bindings.",
                        file=r["file"], line=r["line"],
                        recommendation="Verwende immer Bindings als zweiten Parameter: "
                                       "DB::raw('...', [$value]) oder whereRaw('col = ?', [$value])"
                    ))

    def _check_unescaped_blade(self):
        """Check for unescaped output in Blade templates."""
        results = self._search_files(r"\{!!", "resources/views", [".blade.php", ".php"])
        for r in results:
            self.findings.append(Finding(
                "high", "xss",
                "Unescaped Blade Output {!! !!}",
                f"Unescaped Output kann zu XSS-Angriffen führen: {r['content'][:80]}",
                file=r["file"], line=r["line"],
                recommendation="Verwende {{ }} statt {!! !!}, es sei denn, der Inhalt ist vertrauenswürdig und bereinigt"
            ))

    def _check_mass_assignment(self):
        """Check for mass assignment vulnerabilities."""
        results = self._search_files(r"\$guarded\s*=\s*\[\s*\]", "app/Models", [".php"])
        for r in results:
            self.findings.append(Finding(
                "high", "mass_assignment",
                "Model mit leerem $guarded Array",
                f"$guarded = [] erlaubt Mass Assignment aller Felder.",
                file=r["file"], line=r["line"],
                recommendation="Verwende $fillable mit einer expliziten Liste der erlaubten Felder"
            ))

        # Check for models without $fillable or $guarded
        models_dir = self.project_path / "app" / "Models"
        if models_dir.exists():
            for model_file in models_dir.glob("*.php"):
                content = model_file.read_text(encoding="utf-8", errors="replace")
                if "extends Model" in content or "extends Authenticatable" in content:
                    if "$fillable" not in content and "$guarded" not in content:
                        rel = str(model_file.relative_to(self.project_path))
                        self.findings.append(Finding(
                            "medium", "mass_assignment",
                            f"Model ohne $fillable/$guarded",
                            "Model hat weder $fillable noch $guarded definiert.",
                            file=rel,
                            recommendation="Definiere $fillable mit den erlaubten Feldern"
                        ))

    def _check_env_calls_in_app(self):
        """Check for env() calls outside of config files."""
        results = self._search_files(r"\benv\s*\(", "app", [".php"])
        for r in results:
            # Skip comments
            if r["content"].strip().startswith("//") or r["content"].strip().startswith("*"):
                continue
            self.findings.append(Finding(
                "medium", "config",
                "env() Aufruf außerhalb von config/",
                "env() sollte nur in config/-Dateien verwendet werden. "
                "Nach config:cache funktionieren env()-Aufrufe außerhalb von config/ nicht mehr.",
                file=r["file"], line=r["line"],
                recommendation="Verwende config('key') statt env('KEY') in app/-Dateien"
            ))

    def _check_debug_statements(self):
        """Check for debug statements in code."""
        debug_patterns = [
            (r"\bdd\s*\(", "dd()"),
            (r"\bdump\s*\(", "dump()"),
            (r"\bvar_dump\s*\(", "var_dump()"),
            (r"\bprint_r\s*\(", "print_r()"),
            (r"\bray\s*\(", "ray()"),
        ]

        for pattern, name in debug_patterns:
            results = self._search_files(pattern, "app", [".php"])
            results += self._search_files(pattern, "routes", [".php"])
            for r in results:
                if r["content"].strip().startswith("//"):
                    continue
                self.findings.append(Finding(
                    "medium", "debug",
                    f"Debug-Statement {name} im Code",
                    f"Debug-Ausgabe sollte nicht in Production vorhanden sein.",
                    file=r["file"], line=r["line"],
                    recommendation=f"Entferne {name} vor dem Go-Live"
                ))

    def _check_file_permissions(self):
        """Check critical file permissions."""
        env_file = self.project_path / ".env"
        if env_file.exists():
            mode = oct(env_file.stat().st_mode)[-3:]
            if mode not in ("600", "640", "644"):
                self.findings.append(Finding(
                    "medium", "permissions",
                    f".env Datei hat Berechtigungen {mode}",
                    "Die .env Datei sollte restriktive Berechtigungen haben.",
                    file=".env",
                    recommendation="Setze chmod 640 .env oder chmod 600 .env"
                ))

    def _check_https_enforcement(self):
        """Check if HTTPS is enforced."""
        # Check AppServiceProvider
        provider = self._read_file("app/Providers/AppServiceProvider.php")
        middleware_dir = self.project_path / "app" / "Http" / "Middleware"
        bootstrap_app = self._read_file("bootstrap/app.php")

        https_forced = False
        if provider and "forceScheme" in provider and "https" in provider:
            https_forced = True
        if bootstrap_app and "forceScheme" in bootstrap_app:
            https_forced = True
        if middleware_dir and middleware_dir.exists():
            for f in middleware_dir.glob("*.php"):
                content = f.read_text(encoding="utf-8", errors="replace")
                if "forceScheme" in content or "HttpsProtocol" in content:
                    https_forced = True

        if not https_forced:
            self.findings.append(Finding(
                "high", "transport",
                "HTTPS wird nicht erzwungen",
                "Es wurde keine HTTPS-Erzwingung gefunden.",
                recommendation="Füge URL::forceScheme('https') in AppServiceProvider::boot() hinzu "
                               "oder nutze eine Middleware"
            ))

    def _check_rate_limiting(self):
        """Check rate limiting configuration."""
        # Laravel 11+
        bootstrap_app = self._read_file("bootstrap/app.php")
        # Laravel 10 and below
        route_provider = self._read_file("app/Providers/RouteServiceProvider.php")

        has_rate_limit = False
        if bootstrap_app and "RateLimiter" in bootstrap_app:
            has_rate_limit = True
        if route_provider and "RateLimiter" in route_provider:
            has_rate_limit = True

        # Check for throttle middleware in routes
        route_files = ["routes/web.php", "routes/api.php"]
        for rf in route_files:
            content = self._read_file(rf)
            if content and "throttle" in content:
                has_rate_limit = True

        if not has_rate_limit:
            self.findings.append(Finding(
                "high", "rate_limiting",
                "Kein Rate-Limiting konfiguriert",
                "Ohne Rate-Limiting ist die App anfällig für Brute-Force und DoS-Angriffe.",
                recommendation="Konfiguriere RateLimiter in RouteServiceProvider oder bootstrap/app.php "
                               "und verwende die 'throttle' Middleware auf Login- und API-Routes"
            ))

    def _check_unprotected_routes(self):
        """Check for routes without middleware."""
        route_files = ["routes/web.php", "routes/api.php"]
        for rf in route_files:
            content = self._read_file(rf)
            if not content:
                continue

            # Look for routes that might not have middleware
            # This is a heuristic - routes defined outside of middleware groups
            lines = content.splitlines()
            in_middleware_group = 0
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if "->middleware(" in stripped or "middleware(" in stripped:
                    continue
                if re.search(r"Route::(get|post|put|patch|delete|any|resource)\s*\(", stripped):
                    if in_middleware_group == 0 and "middleware" not in stripped:
                        if not stripped.startswith("//"):
                            self.findings.append(Finding(
                                "medium", "auth",
                                f"Route möglicherweise ohne Middleware",
                                f"Route könnte ohne Auth/Middleware definiert sein: {stripped[:80]}",
                                file=rf, line=i,
                                recommendation="Prüfe ob diese Route Middleware benötigt (auth, verified, etc.)"
                            ))
                if "->group(" in stripped or "::group(" in stripped:
                    in_middleware_group += 1
                if stripped == "});" and in_middleware_group > 0:
                    in_middleware_group -= 1

    def _check_external_resources(self):
        """Check for external CDN resources (DSGVO relevant)."""
        external_patterns = [
            (r"fonts\.googleapis\.com", "Google Fonts"),
            (r"cdn\.jsdelivr\.net", "jsDelivr CDN"),
            (r"cdnjs\.cloudflare\.com", "Cloudflare CDN"),
            (r"unpkg\.com", "unpkg CDN"),
            (r"ajax\.googleapis\.com", "Google Ajax CDN"),
            (r"maxcdn\.bootstrapcdn\.com", "Bootstrap CDN"),
            (r"www\.googletagmanager\.com", "Google Tag Manager"),
            (r"www\.google-analytics\.com", "Google Analytics"),
            (r"connect\.facebook\.net", "Facebook SDK"),
            (r"platform\.twitter\.com", "Twitter/X Platform"),
        ]

        for pattern, name in external_patterns:
            results = self._search_files(pattern, "resources", [".blade.php", ".php", ".html", ".js", ".css"])
            results += self._search_files(pattern, "public", [".html", ".js", ".css"])
            if results:
                self.findings.append(Finding(
                    "medium", "dsgvo",
                    f"Externe Resource: {name}",
                    f"Externe Resource {name} gefunden. Kann DSGVO-relevant sein, "
                    f"da Daten an Drittanbieter übertragen werden.",
                    file=results[0]["file"], line=results[0]["line"],
                    recommendation=f"Hoste {name}-Resources lokal oder stelle sicher, "
                                   f"dass eine DSGVO-konforme Einwilligung eingeholt wird"
                ))

    def _check_composer_audit(self):
        """Run composer audit if available."""
        composer_lock = self.project_path / "composer.lock"
        if not composer_lock.exists():
            self.findings.append(Finding(
                "medium", "dependencies",
                "Keine composer.lock Datei gefunden",
                "Ohne composer.lock können sich Dependencies zwischen Deployments ändern.",
                recommendation="Führe 'composer install' aus und committe die composer.lock"
            ))
            return

        try:
            result = subprocess.run(
                ["composer", "audit", "--format=json", "--no-interaction"],
                capture_output=True, text=True, timeout=30,
                cwd=str(self.project_path)
            )
            if result.returncode != 0 and result.stdout:
                try:
                    audit_data = json.loads(result.stdout)
                    advisories = audit_data.get("advisories", {})
                    for pkg, advs in advisories.items():
                        for adv in advs:
                            self.findings.append(Finding(
                                "high", "dependencies",
                                f"Vulnerability in {pkg}",
                                f"{adv.get('title', 'Unbekannte Vulnerability')} - {adv.get('cve', 'Kein CVE')}",
                                recommendation=f"Update {pkg}: {adv.get('link', '')}"
                            ))
                except json.JSONDecodeError:
                    pass
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self.findings.append(Finding(
                "low", "dependencies",
                "composer audit konnte nicht ausgeführt werden",
                "Composer ist nicht verfügbar oder der Audit hat zu lange gedauert.",
                recommendation="Führe 'composer audit' manuell aus"
            ))

    def _check_storage_links(self):
        """Check if storage is properly linked and configured."""
        public_storage = self.project_path / "public" / "storage"
        if not public_storage.exists() and not public_storage.is_symlink():
            self.findings.append(Finding(
                "low", "config",
                "Storage Symlink fehlt",
                "public/storage Symlink existiert nicht.",
                recommendation="Führe 'php artisan storage:link' aus, falls File-Uploads benötigt werden"
            ))

    def _check_telescope_horizon(self):
        """Check if Telescope/Horizon are properly secured."""
        telescope_config = self._read_file("config/telescope.php")
        if telescope_config:
            if re.search(r"'enabled'\s*=>\s*(?:env\([^)]*,\s*)?true", telescope_config):
                self.findings.append(Finding(
                    "medium", "debug",
                    "Laravel Telescope ist aktiviert",
                    "Telescope sollte in Production deaktiviert oder nur für autorisierte User zugänglich sein.",
                    file="config/telescope.php",
                    recommendation="Setze TELESCOPE_ENABLED=false in .env oder schütze Telescope mit Gate::define"
                ))

        horizon_config = self._read_file("config/horizon.php")
        if horizon_config:
            # Check if Horizon auth is configured
            horizon_provider = self._read_file("app/Providers/HorizonServiceProvider.php")
            if horizon_provider and "gate" not in horizon_provider.lower():
                self.findings.append(Finding(
                    "medium", "auth",
                    "Horizon Gate möglicherweise nicht konfiguriert",
                    "Laravel Horizon sollte über Gate::define in HorizonServiceProvider geschützt werden.",
                    file="app/Providers/HorizonServiceProvider.php",
                    recommendation="Konfiguriere die Gate-Definition in HorizonServiceProvider::gate()"
                ))

    def _check_error_pages(self):
        """Check for custom error pages."""
        error_pages = ["403", "404", "419", "429", "500", "503"]
        errors_dir = self.project_path / "resources" / "views" / "errors"

        missing = []
        for code in error_pages:
            blade_file = errors_dir / f"{code}.blade.php" if errors_dir.exists() else None
            if not blade_file or not blade_file.exists():
                missing.append(code)

        if missing:
            self.findings.append(Finding(
                "low", "error_handling",
                f"Custom Error Pages fehlen: {', '.join(missing)}",
                "Ohne custom Error Pages werden die Default-Laravel-Seiten gezeigt, "
                "die Informationen über das Framework leaken können.",
                recommendation=f"Erstelle Blade-Templates: resources/views/errors/{{{', '.join(missing)}}}.blade.php"
            ))

    def _check_log_config(self):
        """Check logging configuration."""
        env = self._read_file(".env")
        if not env:
            return

        match = re.search(r"^LOG_CHANNEL\s*=\s*(.+)$", env, re.MULTILINE)
        if match:
            channel = match.group(1).strip()
            if channel == "single":
                self.findings.append(Finding(
                    "low", "logging",
                    "LOG_CHANNEL ist 'single'",
                    "Der 'single' Log-Channel erstellt eine einzige Log-Datei, die sehr groß werden kann.",
                    file=".env",
                    recommendation="Verwende LOG_CHANNEL=stack mit daily Channel für Log-Rotation"
                ))

    def _check_cookie_config(self):
        """Check cookie encryption and security."""
        # Check for cookie encryption exceptions
        results = self._search_files(r"encryptCookies|EncryptCookies", "app/Http", [".php"])
        results += self._search_files(r"encryptCookies", "bootstrap", [".php"])

        for r in results:
            if "except" in r["content"].lower():
                self.findings.append(Finding(
                    "medium", "cookies",
                    "Cookie-Verschlüsselungs-Ausnahmen gefunden",
                    "Einige Cookies werden nicht verschlüsselt.",
                    file=r["file"], line=r["line"],
                    recommendation="Prüfe ob alle Cookie-Ausnahmen wirklich nötig sind"
                ))

    def _check_password_config(self):
        """Check password hashing and reset configuration."""
        auth_config = self._read_file("config/auth.php")
        hashing_config = self._read_file("config/hashing.php")

        if hashing_config:
            if re.search(r"'driver'\s*=>\s*(?:env\([^)]*,\s*)?['\"]?md5['\"]?", hashing_config, re.IGNORECASE):
                self.findings.append(Finding(
                    "critical", "auth",
                    "Unsicherer Hashing-Algorithmus (MD5)",
                    "MD5 ist nicht für Passwort-Hashing geeignet.",
                    file="config/hashing.php",
                    recommendation="Verwende bcrypt oder argon2id für Passwort-Hashing"
                ))
            elif re.search(r"'driver'\s*=>\s*(?:env\([^)]*,\s*)?['\"]?sha1['\"]?", hashing_config, re.IGNORECASE):
                self.findings.append(Finding(
                    "critical", "auth",
                    "Unsicherer Hashing-Algorithmus (SHA1)",
                    "SHA1 ist nicht für Passwort-Hashing geeignet.",
                    file="config/hashing.php",
                    recommendation="Verwende bcrypt oder argon2id für Passwort-Hashing"
                ))

    def _check_trusted_proxies(self):
        """Check TrustProxies middleware configuration."""
        # Laravel 11+
        bootstrap_app = self._read_file("bootstrap/app.php")
        if bootstrap_app and "trustProxies" in bootstrap_app:
            if "'*'" in bootstrap_app or '"*"' in bootstrap_app:
                self.findings.append(Finding(
                    "medium", "transport",
                    "TrustProxies vertraut allen Proxies (*)",
                    "Alle Proxies zu vertrauen kann zu IP-Spoofing führen.",
                    file="bootstrap/app.php",
                    recommendation="Beschränke trusted proxies auf die tatsächlichen Proxy-IPs"
                ))

        # Laravel 10 and below
        trust_proxies = self._read_file("app/Http/Middleware/TrustProxies.php")
        if trust_proxies:
            if re.search(r"\$proxies\s*=\s*'\*'", trust_proxies):
                self.findings.append(Finding(
                    "medium", "transport",
                    "TrustProxies vertraut allen Proxies (*)",
                    "Alle Proxies zu vertrauen kann zu IP-Spoofing führen.",
                    file="app/Http/Middleware/TrustProxies.php",
                    recommendation="Beschränke $proxies auf die tatsächlichen Proxy-IPs"
                ))

    def _check_git_secrets(self):
        """Check if .env is in .gitignore."""
        gitignore = self._read_file(".gitignore")
        if gitignore:
            if ".env" not in gitignore:
                self.findings.append(Finding(
                    "critical", "secrets",
                    ".env ist nicht in .gitignore",
                    "Die .env Datei mit allen Secrets könnte im Git-Repository landen.",
                    file=".gitignore",
                    recommendation="Füge .env zur .gitignore hinzu"
                ))
        else:
            self.findings.append(Finding(
                "high", "secrets",
                "Keine .gitignore Datei gefunden",
                "Ohne .gitignore könnten sensible Dateien im Repository landen.",
                recommendation="Erstelle eine .gitignore mit mindestens: .env, vendor/, node_modules/, storage/"
            ))

    def _output_results(self):
        """Output results as JSON."""
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_findings = sorted(self.findings, key=lambda f: severity_order.get(f.severity, 99))

        counts = {
            "critical": sum(1 for f in self.findings if f.severity == "critical"),
            "high": sum(1 for f in self.findings if f.severity == "high"),
            "medium": sum(1 for f in self.findings if f.severity == "medium"),
            "low": sum(1 for f in self.findings if f.severity == "low"),
        }

        result = {
            "project_info": self.info,
            "summary": {
                "total_findings": len(self.findings),
                "counts": counts,
                "go_live_ready": counts["critical"] == 0 and counts["high"] == 0,
            },
            "findings": [f.to_dict() for f in sorted_findings],
        }

        output = json.dumps(result, indent=2, ensure_ascii=False)
        print(output)
        return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 audit.py <laravel-project-path>")
        print("Example: python3 audit.py /home/user/my-laravel-app")
        sys.exit(1)

    project_path = sys.argv[1]
    if not os.path.isdir(project_path):
        print(f"Error: '{project_path}' is not a valid directory")
        sys.exit(1)

    auditor = LaravelSecurityAudit(project_path)
    result = auditor.run()

    # Print summary
    print("\n" + "=" * 60)
    print("📊 AUDIT ZUSAMMENFASSUNG")
    print("=" * 60)
    counts = result["summary"]["counts"]
    print(f"  🔴 Kritisch: {counts['critical']}")
    print(f"  🟠 Hoch:     {counts['high']}")
    print(f"  🟡 Mittel:   {counts['medium']}")
    print(f"  🟢 Niedrig:  {counts['low']}")
    print(f"  {'✅ GO-LIVE READY' if result['summary']['go_live_ready'] else '❌ NICHT GO-LIVE READY'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
