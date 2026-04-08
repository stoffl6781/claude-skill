---
description: "Backend-Regeln für PHP, Laravel, WordPress. Automatisch aktiv bei Backend-Dateien."
globs: "app/**/*.php,routes/**/*.php,database/**/*.php,config/**/*.php"
---

# Backend-Regeln

## PHP Allgemein
- `declare(strict_types=1)` in jeder Datei
- Return Types und Parameter Types immer annotieren
- `const` by default, `let` wenn nötig, `var` niemals (JS)
- Keine globalen Variablen – Dependency Injection

## Laravel
- Business-Logik in Services, nicht Controller
- Form Requests für Validation – keine Inline-Validation
- Policies für Authorization – kein inline `Gate::check`
- Jobs `implements ShouldQueue` – nie synchron bei >200ms
- `config()` statt `env()` in App-Code
- `$fillable` explizit auf jedem Model
- Migrations: Immer `down()` implementieren
- Eager Loading: `.with()` statt N+1

## WordPress
- Hooks vor direkten Calls: `add_action`, `add_filter`
- `$wpdb->prepare()` für alle Queries
- Child-Theme – nie Parent editieren
- `wp_enqueue_script/style` für Assets

## Security (Pflicht)
- Prepared Statements immer (Query Builder/Eloquent)
- `{{ }}` in Blade (kein `{!! !!}` ohne Grund)
- Nonces bei WP-Forms und AJAX
- CSRF automatisch via Middleware
- Rate Limiting auf öffentlichen Endpunkten
- Keine Secrets in Code – immer `.env` / `config()`

## DSGVO
- IP-Anonymisierung in Logs
- Keine externen Ressourcen ohne Consent
- Data Minimization: Nur speichern was nötig
