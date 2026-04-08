---
description: "Security-Regeln für Umgebungsvariablen, Konfiguration, Secrets. Automatisch aktiv bei sensiblen Dateien."
globs: ".env*,config/**/*.php,routes/**/*.php,app/Http/Middleware/**/*.php,next.config.*"
---

# Security-Regeln

## Secrets
- **Nie** hardcodieren – immer `.env` / `config()`
- `.env` in `.gitignore` (PFLICHT)
- `.env.example` ohne echte Werte
- `NEXT_PUBLIC_` / client-seitige Keys: Nur öffentlich sichere Werte
- Änderungen an `.env*` oder Secrets: Explizit User informieren

## Input
- Server-seitige Validierung IMMER (nie nur Client)
- Laravel: Form Requests mit typisierten Rules
- WordPress: `sanitize_text_field()`, `absint()`, etc.
- SQL: Prepared Statements / Query Builder (kein `DB::raw()` mit User-Input)
- XSS: `{{ }}` in Blade, `esc_html()` in WP

## Auth
- Rate Limiting auf Login, Register, Password-Reset
- CSRF auf allen POST/PUT/DELETE Formularen
- Session: `secure`, `httponly`, `samesite=lax`
- 2FA anbieten wo möglich

## Headers
- `X-Frame-Options: DENY` (Clickjacking)
- `X-Content-Type-Options: nosniff`
- `Strict-Transport-Security` mit `includeSubDomains`
- `Referrer-Policy: origin-when-cross-origin`

## DSGVO (Österreich/EU)
- Keine externen Ressourcen ohne Consent (Fonts, CDN, Analytics)
- IP-Anonymisierung in Logs (letztes Oktett maskieren)
- Cookie Consent vor Tracking
- Datenexport (Art. 20) und Löschung (Art. 17) implementieren
- Impressum, Datenschutz, AGB, Widerruf als Pflichtseiten

## Review-Trigger
Diese Änderungen erfordern besondere Aufmerksamkeit:
- Neue Environment-Variablen → In `.env.example` dokumentieren
- Auth-Flow-Änderungen → Security-Implications prüfen
- Neue API-Endpunkte → Rate Limiting + Auth prüfen
- Datenbank-Berechtigungen → Least Privilege
