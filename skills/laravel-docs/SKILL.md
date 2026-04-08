---
name: laravel-docs
description: >
  Generiert Projektdokumentation aus Laravel-Codebases mit MkDocs Material.
  Nutze bei: "Dokumentation erstellen", "Doku generieren", "Server-Doku",
  "Installationsanleitung", "Projekt dokumentieren", "Übergabe-Doku",
  "MkDocs aufsetzen", "welche Cronjobs/Commands gibt es".
---

# Laravel Docs Generator (MkDocs Material)

## Struktur

```
docs/
├── technik/     (Architektur, Models, Routes, Services, Commands, API)
├── server/      (Anforderungen, Installation, Deployment, Cronjobs, Environment)
└── kunde/       (Übersicht, Admin-Bereich, FAQ)
```

## Workflow

1. **Scan:** Routes, Models, Migrations, Commands, Jobs, Config, .env scannen
2. **Validieren:** Alle Migrations gelistet? Commands vollständig? @doc-Tags erfasst?
3. **Generieren:** MkDocs-Seiten pro Bereich schreiben
4. **Build:** `mkdocs build` → `site/` Ordner (in .gitignore!)

## @doc Annotations

Im Code platzieren – wird beim Scan automatisch erfasst:

```php
/** @doc:cron Täglich 3:00 Uhr: Sitemap generieren */

/**
 * @doc:setup
 * composer install && php artisan migrate
 * npm run build
 */

/** @doc:env MAIL_MAILER – smtp für Produktion, log für Entwicklung */
/** @doc:api POST /api/webhook – Mollie Payment Webhook */
/** @doc:admin Unter "Einstellungen" können Firmendaten geändert werden */
```

**Tags:** `@doc:setup`, `@doc:cron`, `@doc:env`, `@doc:api`, `@doc:admin`, `@doc:queue`, `@doc:config`, `@doc:migration`, `@doc:security`, `@doc:performance`, `@doc:troubleshoot`

## Scan-Befehle

```bash
php artisan route:list --json
ls app/Models/
ls app/Console/Commands/
grep -r "@doc:" app/ config/ routes/ --include="*.php"
php artisan schedule:list
cat .env.example
```

## Content pro Seite

| Seite | Quelle | Inhalt |
|---|---|---|
| architektur.md | Code-Analyse | Ordnerstruktur, Patterns, Tech-Stack |
| models.md | `app/Models/` | Relationen, Scopes, Casts, Factories |
| routes.md | `route:list` | Gruppiert nach Prefix, Middleware |
| services.md | `app/Services/` | Public Methods, Abhängigkeiten |
| commands.md | `Commands/` + `schedule:list` | Signatur, Beschreibung, Schedule |
| installation.md | @doc:setup + .env.example | Schritt-für-Schritt |
| environment.md | .env.example + @doc:env | Alle Variablen mit Erklärung |
| cronjobs.md | schedule:list + @doc:cron | Frequenz, Zweck |

## MkDocs Setup

```yaml
# mkdocs.yml (Minimal)
site_name: "{Projekt} Dokumentation"
theme:
  name: material
  language: de
  features: [navigation.sections, navigation.expand, search.highlight]
nav:
  - Start: index.md
  - Technik: [technik/architektur.md, technik/models.md, technik/routes.md]
  - Server: [server/installation.md, server/environment.md, server/cronjobs.md]
  - Kunde: [kunde/uebersicht.md, kunde/admin-bereich.md]
```

## Deployment

```bash
mkdocs build                    # Generiert site/
mkdocs gh-deploy                # GitHub Pages
# oder: scp -r site/* user@server:/var/www/docs/
```
