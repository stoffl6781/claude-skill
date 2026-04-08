---
name: audit-project
description: "Bestehendes Projekt analysieren und auf Qualitätsstandard bringen: fehlende Struktur, Rules, Tests, Security, A11y. Nutze bei: 'Projekt prüfen', 'was fehlt hier', 'Projekt aufräumen', 'auf Standard bringen', 'Audit', 'Qualität prüfen'."
---

# /audit-project – Bestehendes Projekt auf Standard bringen

Du analysierst ein bestehendes Projekt und identifizierst was fehlt, um es auf den definierten Qualitätsstandard zu heben.

## Workflow

### 1. Stack & Zustand erkennen

```bash
echo "=== STACK ==="
ls composer.json artisan 2>/dev/null && echo "LARAVEL"
ls style.css functions.php 2>/dev/null && echo "WORDPRESS"
ls package.json next.config.* nuxt.config.* 2>/dev/null && echo "NODE"
ls tsconfig.json 2>/dev/null && echo "TYPESCRIPT"
ls tailwind.config.* 2>/dev/null && echo "TAILWIND"

echo "=== PROJEKT-GRÖSSE ==="
find app -name "*.php" 2>/dev/null | wc -l
find resources/views -name "*.blade.php" 2>/dev/null | wc -l
find src -name "*.tsx" -o -name "*.vue" 2>/dev/null | wc -l
git rev-list --count HEAD 2>/dev/null || echo "Kein Git"

echo "=== BESTEHENDE QUALITÄT ==="
ls .claude/ 2>/dev/null && echo "Hat .claude/" || echo "FEHLT: .claude/"
ls CLAUDE.md 2>/dev/null && echo "Hat CLAUDE.md" || echo "FEHLT: CLAUDE.md"
ls features/INDEX.md 2>/dev/null && echo "Hat Feature-Tracking" || echo "FEHLT: Feature-Tracking"
ls .claude/rules/ 2>/dev/null && echo "Hat Rules" || echo "FEHLT: Rules"
find tests -name "*.php" 2>/dev/null | wc -l || echo "FEHLT: Tests"
ls .env.example 2>/dev/null && echo "Hat .env.example" || echo "FEHLT: .env.example"
ls .gitignore 2>/dev/null && echo "Hat .gitignore" || echo "FEHLT: .gitignore"
```

### 2. Audit-Checkliste durchgehen

Prüfe JEDE Kategorie und bewerte mit ✅ (vorhanden), ⚠️ (teilweise), ❌ (fehlt):

#### A) Projekt-Struktur
- [ ] `.claude/` Ordner mit Rules
- [ ] `CLAUDE.md` mit Projektbeschreibung und Stack
- [ ] `features/INDEX.md` für Feature-Tracking
- [ ] `.claude/settings.json` mit Permissions
- [ ] `.env.example` vollständig und ohne echte Secrets
- [ ] `.gitignore` korrekt (vendor, node_modules, .env, logs)

#### B) Code-Qualität
- [ ] Konsistenter Code-Style (Pint, ESLint, Prettier)
- [ ] Keine `dd()`, `dump()`, `var_dump()`, `console.log()` im Code
- [ ] Keine hardcodierten Secrets
- [ ] Strict Types (PHP) / Strict Mode (TS)
- [ ] Sinnvolle Variablen- und Funktionsnamen
- [ ] Kommentare erklären Warum, nicht Was

#### C) Security
- [ ] CSRF-Schutz aktiv
- [ ] Rate Limiting auf Auth-Endpunkten
- [ ] Authorization (Policies/Guards/Capabilities)
- [ ] Input Validation (Form Requests / Sanitizing)
- [ ] HTTPS erzwungen (Production)
- [ ] Keine SQL-Injection-Risiken (Prepared Statements)
- [ ] Security Headers (X-Frame-Options, HSTS, etc.)

#### D) Testing
- [ ] Tests existieren überhaupt
- [ ] Auth-Tests (Login, Register, Rollen)
- [ ] Business-Logik-Tests (Services, Models)
- [ ] Security-Tests (Authorization, CSRF, Injection)
- [ ] Tests laufen grün (`php artisan test` / `npm test`)

#### E) Frontend / A11y
- [ ] Semantisches HTML (keine div-Buttons)
- [ ] Heading-Hierarchie (h1 → h2 → h3)
- [ ] Alle Inputs haben Labels
- [ ] Alt-Texte auf Bildern
- [ ] Focus-Ring sichtbar
- [ ] Responsive (Mobile, Tablet, Desktop)
- [ ] Dark Mode (wenn im Projekt)
- [ ] Loading/Empty/Error States

#### F) Internationalisierung
- [ ] Strings übersetzbar (nicht hardcodiert)
- [ ] Sprachdateien vorhanden
- [ ] Locale-Switching funktioniert

#### G) Deployment-Readiness
- [ ] `APP_DEBUG=false` für Production dokumentiert
- [ ] Queue-System konfiguriert
- [ ] Cache-Strategie vorhanden
- [ ] Backup-Strategie dokumentiert
- [ ] Error-Monitoring geplant (Sentry etc.)

#### H) Dokumentation
- [ ] README oder CLAUDE.md beschreibt wie man das Projekt startet
- [ ] API-Dokumentation (wenn API vorhanden)
- [ ] Deployment-Anleitung

#### I) Plugins & Erweiterungen
Prüfe ob die empfohlenen Claude-Plugins installiert sind:

```bash
cat ~/.claude/settings.json | grep -o '"[a-z-]*@[a-z-]*": true' | sort
```

**Pflicht-Plugins:**

| Plugin | Zweck | Installieren |
|---|---|---|
| `superpowers@superpowers-marketplace` | Brainstorming, Plans, Debugging, Code Review | `claude plugins add superpowers@superpowers-marketplace` |
| `ui-ux-pro-max@ui-ux-pro-max-skill` | Design-Stile, Farben, Fonts, UX-Guidelines | `claude plugins add ui-ux-pro-max@ui-ux-pro-max-skill` |
| `claude-mem@thedotmack` | Persistentes Gedächtnis über Sessions | `claude plugins add claude-mem@thedotmack` |

**Empfohlen für Frontend-Projekte:**

| Plugin | Zweck | Installieren |
|---|---|---|
| `frontend-design@claude-code-plugins` | Production-grade UI | `claude plugins add frontend-design@claude-code-plugins` |
| `superpowers-chrome@superpowers-marketplace` | Browser-Steuerung/Testing | `claude plugins add superpowers-chrome@superpowers-marketplace` |

**Empfohlen für Code-Qualität:**

| Plugin | Zweck | Installieren |
|---|---|---|
| `code-review@claude-code-plugins` | PR Reviews | `claude plugins add code-review@claude-code-plugins` |
| `feature-dev@claude-code-plugins` | Guided Development | `claude plugins add feature-dev@claude-code-plugins` |
| `security-guidance@claude-code-plugins` | Security-Patterns | `claude plugins add security-guidance@claude-code-plugins` |
| `elements-of-style@superpowers-marketplace` | Besseres Schreiben | `claude plugins add elements-of-style@superpowers-marketplace` |

Fehlende Pflicht-Plugins als **kritische Lücke** melden, empfohlene als **Verbesserung**.

### 3. Ergebnis-Report

Erstelle einen Report in diesem Format:

```markdown
# Projekt-Audit: {Name}

**Datum:** {YYYY-MM-DD}
**Stack:** {erkannter Stack}
**Größe:** {X Models, Y Views, Z Commits}

## Gesamtbewertung: {Score}/100

| Kategorie | Status | Score |
|-----------|--------|-------|
| A) Projekt-Struktur | {✅/⚠️/❌} | {X}/15 |
| B) Code-Qualität | {✅/⚠️/❌} | {X}/15 |
| C) Security | {✅/⚠️/❌} | {X}/20 |
| D) Testing | {✅/⚠️/❌} | {X}/15 |
| E) Frontend / A11y | {✅/⚠️/❌} | {X}/15 |
| F) Internationalisierung | {✅/⚠️/❌} | {X}/5 |
| G) Deployment-Ready | {✅/⚠️/❌} | {X}/10 |
| H) Dokumentation | {✅/⚠️/❌} | {X}/5 |

## Kritische Lücken (sofort beheben)
1. {Problem} → {Fix}

## Empfohlene Verbesserungen (wichtig)
1. {Problem} → {Fix}

## Nice-to-have (wenn Zeit)
1. {Verbesserung}

## Aktionsplan
| # | Aktion | Skill | Aufwand |
|---|--------|-------|---------|
| 1 | {Was} | `/init-project` | {Zeit} |
| 2 | {Was} | `/laravel-security-audit` | {Zeit} |
| 3 | {Was} | `/laravel-tests` | {Zeit} |
```

### 4. Fehlende Struktur anbieten

Nach dem Report fragen:

> Soll ich die fehlende Projekt-Struktur jetzt anlegen?
> - `.claude/` Ordner mit Rules → Ja/Nein
> - `CLAUDE.md` → Ja/Nein
> - `features/INDEX.md` → Ja/Nein
> - Fehlende `.env.example` Einträge → Ja/Nein

Wenn User bestätigt → die Dateien generieren (wie `/init-project`, aber nur die fehlenden Teile).

### 5. Follow-Up Skills empfehlen

Basierend auf den Lücken, die passenden Skills empfehlen:

| Lücke | Empfohlener Skill |
|---|---|
| Keine Tests | → `/laravel-tests` |
| Security-Probleme | → `/laravel-security-audit` |
| Performance-Probleme | → `/laravel-performance` |
| A11y-Probleme | → `/laravel-a11y` |
| Kein SEO | → `/seo` |
| Keine GEO-Optimierung | → `/geo` |
| Kein Feature-Tracking | → `/requirements` für offene Features |
| Kein Deployment-Plan | → `/deploy` |

## Regeln

1. **Ehrlich bewerten**: Kein Schönreden. Wenn Security fehlt, ist das kritisch
2. **Priorisieren**: Kritisch → Wichtig → Nice-to-have. Nicht alles auf einmal
3. **Nicht automatisch fixen**: Erst Report zeigen, dann User entscheiden lassen
4. **Bestehendes respektieren**: Projekt hat Konventionen? Übernehmen, nicht ersetzen
5. **Realistisch**: Ein WordPress-Blog braucht kein Redis + Horizon. Empfehlungen an Projektgröße anpassen
