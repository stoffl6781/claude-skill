---
name: laravel-performance
description: >
  Performance-Audit für Laravel. Ziel: jede Seite unter 2 Sekunden.
  Nutze bei: "Performance", "Seite ist langsam", "Ladezeit", "Caching",
  "N+1", "Query optimieren", "PageSpeed", "Core Web Vitals", "TTFB",
  "zu viele Queries", "Cache aufsetzen", "Bilder optimieren", "lazy loading",
  "OPcache", "Redis", "CDN".
---

# Laravel Performance Audit

Ziel: **Jede Seite unter 2 Sekunden** (TTFB < 500ms, LCP < 2.0s).

## Performance-Budget

| Metrik | Ziel | Kritisch |
|---|---|---|
| TTFB | < 200ms | > 500ms |
| FCP | < 1.0s | > 2.0s |
| LCP | < 2.0s | > 3.0s |
| CLS | < 0.1 | > 0.25 |
| INP | < 200ms | > 500ms |
| Page Size | < 500KB | > 1.5MB |
| Requests | < 25 | > 50 |
| DB Queries/Request | < 10 | > 30 |

> Core Web Vitals sind auch **SEO-Ranking-Faktor** → SEO Skill.

## Workflow

1. MESSEN → Baseline (vorher)
2. BACKEND → Queries, Caching, PHP
3. FRONTEND → Assets, Bilder, Fonts
4. SERVER → OPcache, Compression, CDN
5. MESSEN → Nachher vergleichen
6. REPORT → Verbesserungen dokumentieren

## 1. Baseline messen

```bash
# Laravel Debug Bar aktivieren (nur lokal!)
# Oder: php artisan debugbar:enable

# Response-Zeiten messen
curl -o /dev/null -s -w "TTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" {URL}

# DB Queries zählen (Telescope oder Debugbar)
```

## 2. Backend-Optimierung

**N+1 Queries finden und fixen:**
```php
// VORHER (N+1)
$posts = Post::all();
$posts->each(fn($p) => $p->author->name);

// NACHHER (Eager Loading)
$posts = Post::with('author')->get();
```

**Caching:**
```php
Cache::remember('key', 3600, fn() => expensiveQuery());

// Laravel Caches
php artisan config:cache    // Config
php artisan route:cache     // Routes
php artisan view:cache      // Views
php artisan event:cache     // Events
```

**Indexes:** `EXPLAIN` auf langsame Queries, fehlende Indexes in Migration hinzufügen.

**DB-Tuning (große Tabellen >1M Zeilen):**
- Partitioning nach Datum
- Read Replicas für SELECT-lastige Apps
- Connection Pooling (ProxySQL/PgBouncer)

## 3. Frontend-Optimierung

**Vite:**
```js
// vite.config.js – Code Splitting
build: { rollupOptions: { output: { manualChunks: { vendor: ['alpinejs'] }}}}
```

**Bilder:** WebP/AVIF, lazy loading (`loading="lazy"`), richtige Größen (srcset), Spatie MediaLibrary Conversions.

**Fonts:** Lokal hosten, `font-display: swap`, nur benötigte Weights, preload im `<head>`.

**CSS/JS:** Purge unused CSS (Tailwind macht das), defer/async für Scripts.

## 4. Server-Optimierung

**OPcache:** `opcache.enable=1`, `opcache.memory_consumption=256`, `opcache.jit=1255`

**Compression:** Brotli > Gzip in nginx/Apache.

**Cache Headers:**
```
# Vite Assets (hashed filenames)
Cache-Control: public, max-age=31536000, immutable

# HTML
Cache-Control: no-cache
```

**CDN (Cloudflare empfohlen):**
- Image Optimization (WebP), Brotli, Page Caching
- DSGVO: Cloudflare mit EU-Rechenzentren konfigurieren

## 5. Monitoring

- **Sentry** – Error + Performance Monitoring
- **Lighthouse CI** – Automatische PageSpeed-Reports in CI
- **Laravel Telescope** – Query/Request Profiling (nur lokal)

## Pest Performance-Tests

```php
it('homepage responds under 500ms', function () {
    $start = microtime(true);
    $this->get('/')->assertOk();
    expect(microtime(true) - $start)->toBeLessThan(0.5);
});

it('homepage uses less than 15 queries', function () {
    DB::enableQueryLog();
    $this->get('/');
    expect(DB::getQueryLog())->toHaveCount(lessThan: 15);
});
```

## Report-Format

```
# Performance Report – {Projekt}

| Metrik | Vorher | Nachher | Budget |
|--------|--------|---------|--------|
| TTFB   | 450ms  | 120ms   | <200ms |
| LCP    | 3.2s   | 1.8s    | <2.0s  |
| Queries| 47     | 8       | <10    |
```
