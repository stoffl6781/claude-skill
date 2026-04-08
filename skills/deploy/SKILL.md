---
name: deploy
description: "Go-Live Checkliste und Deployment. Nutze bei: 'deployen', 'go live', 'Production', 'Launch', 'Release', 'ist die App bereit', 'Deployment Checkliste'."
---

# /deploy – Deployment & Go-Live

Du bist DevOps-Engineer. Du stellst sicher, dass das Deployment sauber läuft.

## Vor dem Start

1. **QA-Status prüfen**: Feature getestet? Keine kritischen Bugs?
2. **Tests**: Alle grün?
3. **Build**: Kompiliert fehlerfrei?

Falls QA nicht gemacht:
> QA wurde noch nicht durchgeführt. Zuerst `/qa` ausführen.

## Pre-Deployment Checklist

### Code-Qualität
```bash
# Tests
php artisan test --parallel 2>/dev/null || npm test 2>/dev/null
# Lint
vendor/bin/pint --test 2>/dev/null || npm run lint 2>/dev/null
# Build
npm run build 2>/dev/null
php artisan view:cache 2>/dev/null
```

- [ ] Alle Tests grün
- [ ] Linter ohne Fehler
- [ ] Build erfolgreich
- [ ] Kein `dd()`, `dump()`, `var_dump()` im Code
- [ ] Keine `console.log()` in Production-JS
- [ ] Code committed und gepusht

### Umgebung (Laravel)
- [ ] `APP_ENV=production`
- [ ] `APP_DEBUG=false`
- [ ] `APP_KEY` gesetzt (nicht der aus .env.example)
- [ ] `APP_URL` korrekt (mit https://)
- [ ] `LOG_LEVEL=warning` (nicht debug)
- [ ] `MAIL_MAILER=smtp` (nicht log/mailtrap)
- [ ] `SESSION_DRIVER=redis` (nicht file)
- [ ] `CACHE_STORE=redis` (nicht file)
- [ ] `QUEUE_CONNECTION=redis` (nicht sync)

### Datenbank
- [ ] Backup erstellt (BEVOR Migration!)
- [ ] `php artisan migrate --force` erfolgreich
- [ ] Keine offenen Migrations die nicht committed sind

### Security
- [ ] SSL-Zertifikat gültig
- [ ] HTTPS erzwungen (`URL::forceScheme('https')`)
- [ ] Mollie Live-Key (nicht test_)
- [ ] `.env` nicht im Webroot erreichbar
- [ ] `.env` nicht in Git
- [ ] Keine Secrets in Code hardcodiert
- [ ] Rate Limiting auf Login/API aktiv

### Performance (Laravel)
```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan event:cache
php artisan optimize
```

### Queue & Scheduler
- [ ] Horizon/Worker läuft (`php artisan horizon`)
- [ ] Supervisor/systemd konfiguriert (Auto-Restart)
- [ ] Scheduler in Crontab: `* * * * * php artisan schedule:run`
- [ ] Jobs verarbeiten korrekt (Horizon Dashboard prüfen)

### Assets
- [ ] `npm run build` (minified, versioned)
- [ ] Keine lokalen Fonts/Scripts von externen CDNs (DSGVO!)
- [ ] Bilder optimiert (WebP/AVIF)

## Deployment-Schritte

### Laravel (typisch)
```bash
# 1. Maintenance Mode
php artisan down --retry=60

# 2. Code holen
git pull origin main

# 3. Dependencies
composer install --no-dev --optimize-autoloader
npm ci && npm run build

# 4. Migrationen
php artisan migrate --force

# 5. Cache
php artisan optimize

# 6. Queue restart
php artisan queue:restart
php artisan horizon:terminate  # Supervisor startet neu

# 7. Online
php artisan up
```

### WordPress (typisch)
```bash
# 1. Backup (DB + Files)
# 2. Plugins deaktivieren
# 3. Updates einspielen (Core, Plugins, Theme)
# 4. Child-Theme prüfen
# 5. Plugins aktivieren
# 6. Cache leeren
# 7. Testen
```

## Post-Deployment

### Sofort prüfen (erste 15 Minuten)
- [ ] Startseite lädt
- [ ] Login funktioniert
- [ ] Hauptfeature funktioniert (1x durchklicken)
- [ ] E-Mails werden versendet (Test-Mail)
- [ ] Queue verarbeitet Jobs (Horizon Dashboard)
- [ ] Keine Errors in Log (`tail -f storage/logs/laravel.log`)
- [ ] SSL funktioniert (kein Mixed Content)

### Monitoring einrichten
- [ ] Error-Tracking (Sentry / Bugsnag)
- [ ] Uptime-Monitoring (UptimeRobot / Betterstack)
- [ ] Log-Rotation konfiguriert
- [ ] Backup-Schedule verifiziert

## Rollback-Plan

Falls etwas schiefgeht:

```bash
# Laravel
php artisan down
git checkout {vorheriger-commit}
composer install --no-dev --optimize-autoloader
php artisan migrate:rollback
php artisan optimize
php artisan up
```

## Ergebnis in Feature-Spec

```markdown
## Deployment

**Deployed:** {YYYY-MM-DD}
**Umgebung:** Production
**URL:** {https://...}
**Status:** Live
**Rollback:** {commit-hash falls nötig}
```

## INDEX aktualisieren

Status des Features auf **Done** setzen.
