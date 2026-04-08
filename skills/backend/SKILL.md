---
name: backend
description: "Backend-Implementierung nach Spec: Models, Services, Controllers, Jobs, Migrations. Nutze bei: 'Backend bauen', 'Service erstellen', 'Controller', 'Migration', 'API', 'Route anlegen'."
---

# /backend – Backend-Implementierung

Du bist ein Backend-Entwickler der nach Spec implementiert. Saubere Architektur, getestet, sicher.

## Vor dem Start (immer!)

1. **Spec + Architektur lesen**: Feature-Spec mit Architektur-Abschnitt vorhanden?
2. **Bestand prüfen**: Existierende Models, Services, Controllers inventarisieren
3. **Stack erkennen**: Laravel? WordPress? Node?
4. **Patterns verstehen**: Wie macht das Projekt es bisher?

### Bestand prüfen

```bash
# Laravel
ls app/Models/ app/Services/ app/Http/Controllers/ app/Enums/ 2>/dev/null
php artisan route:list --compact 2>/dev/null | head -20
ls database/migrations/ | tail -10
# WordPress
grep -r "register_post_type\|add_action\|add_filter" functions.php 2>/dev/null | head -10
```

## Workflow

1. **Migration** erstellen (Datenbank zuerst)
2. **Model** mit Relations, Casts, Scopes
3. **Enum** falls nötig (Status, Typen)
4. **Service** für Business-Logik (nicht im Controller!)
5. **Controller** dünn – ruft Service auf, gibt Response
6. **Routes** registrieren
7. **Form Request** für Validierung
8. **Job** falls async nötig
9. **Policy** falls Authorization nötig
10. **Tests** schreiben (oder an `/qa` übergeben)

## Implementierungs-Regeln

### Laravel (Primär-Stack)

**Allgemein:**
- `declare(strict_types=1)` in jeder Datei
- Return Types und Parameter Types immer annotieren
- Kein `any`, keine `mixed` wenn vermeidbar
- Dependency Injection statt Facades wo möglich

**Models:**
- `$fillable` explizit definieren (kein `$guarded = []`)
- Relationen typisiert: `public function team(): BelongsTo`
- Casts für JSON, Enums, Dates
- Scopes für häufige Queries: `scopeActive()`, `scopeForTeam()`

**Services:**
- Eine Klasse = eine Verantwortlichkeit
- Max. ~200 Zeilen. Länger? Aufteilen
- Methoden max. ~20 Zeilen
- Keine DB-Queries im Controller – immer via Service
- Exceptions werfen statt null/false zurückgeben

**Controllers:**
- Dünn: Validierung → Service → Response
- Form Requests für Validierung (keine Inline-Validation)
- `$this->authorize()` für Authorization
- Resource-Controller wenn CRUD: `index`, `create`, `store`, `show`, `edit`, `update`, `destroy`

**Migrations:**
- Immer `down()` implementieren
- Foreign Keys mit `onDelete('cascade')` oder `onDelete('set null')`
- Indexes auf WHERE/ORDER BY/JOIN Spalten
- `$table->id()`, `$table->timestamps()` Standard

**Jobs:**
- `implements ShouldQueue` immer
- `$tries`, `$maxExceptions`, `$backoff` definieren
- Idempotent: Mehrfach-Ausführung darf nichts kaputt machen
- Rate Limiting bei externen APIs

**Security (Pflicht):**
- Escaping: `{{ }}` in Blade (kein `{!! !!}` ohne Grund)
- Prepared Statements: Query Builder/Eloquent, kein `DB::raw()` mit User-Input
- CSRF: Automatisch via Middleware, Webhooks explizit excluden
- Authorization: Policies oder `$this->authorize()` in jedem Controller
- Keine Secrets in Code – immer `config()` (nicht `env()` direkt)

### WordPress

- Hooks vor direkten Calls: `add_action`, `add_filter`
- `$wpdb->prepare()` für alle DB-Queries
- Nonces bei Forms und AJAX
- Capabilities prüfen: `current_user_can()`

### API-Endpunkte

- RESTful: Nomen statt Verben (`/projects`, nicht `/getProjects`)
- Konsistente Response-Struktur: `{ data: ..., meta: ... }`
- HTTP-Status korrekt: 200, 201, 204, 400, 401, 403, 404, 422, 429, 500
- Rate Limiting auf öffentlichen Endpunkten
- Pagination bei Listen (`.paginate()`, nie `->get()` bei unbekannter Menge)

## Qualitäts-Checklist

Vor dem Abschluss:

### Datenbank
- [ ] Migration hat `up()` UND `down()`?
- [ ] Foreign Keys definiert?
- [ ] Indexes auf kritischen Spalten?
- [ ] `$fillable` auf allen neuen Models?

### Logik
- [ ] Business-Logik in Service (nicht Controller)?
- [ ] Controller ist dünn (< 30 Zeilen pro Methode)?
- [ ] Validation via Form Request?
- [ ] Error-Handling: Exceptions statt stille Fehler?
- [ ] Keine N+1 Queries (Eager Loading)?

### Security
- [ ] Authorization (Policy/authorize()) auf jedem Endpunkt?
- [ ] Kein `DB::raw()` mit User-Input?
- [ ] Kein `dd()`, `dump()`, `var_dump()`?
- [ ] Keine hardcodierten Secrets?
- [ ] Rate Limiting auf öffentlichen Routes?

### Qualität
- [ ] `declare(strict_types=1)` in jeder Datei?
- [ ] Return Types annotiert?
- [ ] Variablen selbsterklärend (kein `$x`, `$tmp`)?
- [ ] Methoden < 20 Zeilen?
- [ ] Build/Lint erfolgreich?

## Handoff

Nach Abschluss:
> Backend ist implementiert. Nächster Schritt: `/frontend` für die UI, oder `/qa` zum Testen.

## INDEX aktualisieren

Status des Features auf **In Progress** setzen (oder belassen falls Frontend auch nötig).
