---
name: laravel-security-audit
description: >
  Security-Audit für Laravel-Apps. Nutze bei: "Security Audit",
  "Sicherheitsprüfung", "Go-Live Checkliste", "ist die App sicher",
  "Pre-Launch Check", "DSGVO-Check", "Security Hardening".
---

# Laravel Security Audit

Allgemeine Security-Regeln → **CLAUDE.md Kapitel 1 + 2**. Dieser Skill fokussiert auf Audit-Methodik.

## Severity Framework

| Level | Bedeutung | Zeitrahmen |
|---|---|---|
| KRITISCH | Muss vor Go-Live behoben sein | Sofort |
| HOCH | Ernstes Risiko | Innerhalb 1 Woche |
| MITTEL | Verbesserungspotenzial | Nächster Sprint |
| NIEDRIG | Best Practice | Backlog |

## Workflow

1. **Automatisiert:** `composer audit` + `npm audit` für Dependency-Checks
2. **Manuell:** Checkliste unten durchgehen
3. **Report:** Priorisierte Findings mit konkreten Fixes

## Checkliste

### KRITISCH

**Auth & Authorization:**
- Alle sensiblen Routes durch Middleware geschützt? (`auth`, `verified`, `can:`)
- Rate-Limiting auf Login? (`throttle` Middleware)
- Password-Hashing: bcrypt/argon2 (nie MD5/SHA1)
- Policies für Authorization (nicht `Gate::check` im Blade)

**Injection:**
- Kein rohes SQL – immer Query Builder / Eloquent
- Blade `{{ }}` überall (kein `{!! !!}` ohne Grund)
- Keine gefährlichen PHP-Funktionen mit User-Input

**Environment:**
- `APP_DEBUG=false` in Production
- `APP_ENV=production`
- `.env` nicht in Git, nicht im Webroot
- Keine Secrets in Code hardcodiert

### HOCH

**Mass Assignment:** `$fillable` oder `$guarded` auf allen Models
**CSRF:** `@csrf` in allen Formularen
**File Uploads:** Typ-Validierung, Größenlimit, nicht in `/public` direkt
**Session:** `secure`, `httponly`, `samesite=lax` in `config/session.php`
**API:** Sanctum/Passport für Auth, Rate-Limiting auf allen Endpoints
**Headers:** `X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`

### MITTEL

**Dependencies:** `composer audit` + `npm audit` – kritische sofort, Rest im nächsten Release
**Logging:** Keine Passwörter/IBAN/Keys loggen, IPs anonymisieren
**Error Handling:** Keine Stack-Traces in Production

## DSGVO-spezifisch

**Lösch-Routine (Anonymisierung statt hartem Löschen):**
```php
$user->update([
    'name' => 'Gelöschter Nutzer',
    'email' => "deleted_{$user->id}@example.com",
    'phone' => null,
]);
```

**IP-Anonymisierung in Logs:**
```php
$anonymizedIp = preg_replace('/\d+$/', 'x', $request->ip());
```

**Prüfpunkte:**
- Keine externen Ressourcen ohne Consent (Fonts, Analytics, CDN)
- Cookie-Consent vor Tracking-Code
- Datenschutzerklärung mit allen genutzten Diensten

## Report-Format

```markdown
# Security Audit – {Projekt} ({Datum})

## Zusammenfassung
{X} Kritisch, {Y} Hoch, {Z} Mittel

## Findings
| # | Severity | Kategorie | Finding | Datei | Empfehlung |
|---|----------|-----------|---------|-------|------------|
| 1 | KRITISCH | Auth | Routes ohne Middleware | routes/web.php | auth Middleware |
```
