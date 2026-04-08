---
name: seo
description: >
  Klassisches SEO für Laravel-Projekte: robots.txt, sitemap.xml, Meta-Tags,
  Open Graph, Structured Data (JSON-LD), hreflang, Focus-Keywords, Redirects.
  Nutze bei: "SEO", "Suchmaschinenoptimierung", "robots.txt", "sitemap",
  "Open Graph", "OG Tags", "Meta Tags", "Structured Data", "JSON-LD",
  "Schema.org", "hreflang", "Focus Keyword", "SEO Audit", "SEO Check",
  "SERP", "Google Search Console", "ranking verbessern", "Canonical URL",
  "Rich Snippets", "Meta Description", "SEO generieren".
  Für KI-Auffindbarkeit (ai.txt, llms.txt) → GEO Skill.
---

# SEO – Search Engine Optimization

Für Google, Bing, DuckDuckGo, Yandex, Ecosia.
Für KI-Auffindbarkeit → **GEO Skill**. Wenn User "SEO" sagt, prüfe ob GEO auch relevant ist.

## Workflow

| Schritt | Prüfen |
|---|---|
| 1. Analyse | robots.txt, sitemap, Meta-Tags, OG, JSON-LD, SEO-Felder auf Models |
| 2. Discovery | robots.txt dynamisch via Route, sitemap.xml dynamisch + gecacht |
| 3. Meta-Tags | title, description, canonical, hreflang, geo-targeting, OG, Twitter Cards |
| 4. Structured Data | JSON-LD pro Seitentyp (Organization, Article, Product, FAQ, Breadcrumb) |
| 5. Content | SEO-Felder auf Models, Focus-Keyword-Analyse, KI-Generierung |
| 6. Redirects | 301 für alte URLs, nie 302 für permanente Weiterleitungen |
| 7. Validierung | Rich Results Test, Schema.org Validator, OG Debugger |

> **Core Web Vitals sind Ranking-Faktor.** Für Performance-Optimierung → laravel-perf Skill.

## robots.txt (Dynamisch)

```
Route: GET /robots.txt → gecacht 1h
- User-agent: * / Allow: / / Disallow: /admin/, /api/, /livewire/
- Sitemap: {APP_URL}/sitemap.xml
- APP_ENV=local → Disallow: /
- NIEMALS statische Datei in /public/
- Für KI-Crawler → GEO Skill
```

## Sitemap (Dynamisch)

```
Route: GET /sitemap.xml (Index) + /sitemap-{locale}.xml (pro Sprache)
Cache: 1h, invalidieren bei Content-Änderung
- Nur publizierte Inhalte, <lastmod> aus updated_at
- hreflang-Annotations in Sitemap (xhtml:link)
- Max 50.000 URLs pro Sitemap
```

**Priorities:** Homepage 1.0, Archive 0.8-0.9, Details 0.6-0.8, Statisch 0.3-0.5

## Meta-Tags (im `<head>`)

```html
<title>{meta_title} - {site_name}</title>          <!-- max 60 Zeichen -->
<meta name="description" content="{...}">           <!-- max 155 Zeichen -->
<link rel="canonical" href="{canonical_url}">
<link rel="alternate" hreflang="de" href="{de_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{default_url}">
<meta name="geo.region" content="AT">
<meta name="google-site-verification" content="{aus Settings}">
```

## Open Graph + Twitter

```html
<meta property="og:type" content="{website|article|product}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{1200x630, lokal, max 300KB}">
<meta property="og:image:alt" content="{alt}">
<meta property="og:locale" content="{de_AT|en_US}">
<meta name="twitter:card" content="summary_large_image">
```

**og:type pro Seite:** Homepage→website, Blog→article, Produkt→product

## Structured Data (JSON-LD)

Nur die wichtigsten – projekt-spezifische (LocalBusiness, TouristAttraction, Event etc.) je nach Bedarf ergänzen:

- **Homepage:** Organization (name, url, logo, sameAs)
- **Blog:** Article (headline, datePublished, author, image)
- **Alle Seiten:** BreadcrumbList
- **FAQ-Sektionen:** FAQPage
- **Produkte:** Product (name, offers, price)

Validieren: Google Rich Results Test + Schema.org Validator

## SEO-Felder pro Model

```
meta_title (translatable, max 60 Zeichen)
meta_description (translatable, max 155 Zeichen)
focus_keyword (1-3 Wörter)
```

**Focus-Keyword Score (0-100):** Keyword in Titel (15), Description (15), URL (10), Intro (10), Content (10), Länge ≥600 (10), H2-H4 (10), Titel ≤60 (10), Description ≤155 (10)

**KI-Generierung:** "SEO generieren" Button → Queue-Job → füllt fehlende Felder. Batch über SEO-Dashboard.

## Redirects

```php
// 301 für permanente Weiterleitungen (alte URLs, Slug-Änderungen)
Route::redirect('/alter-pfad', '/neuer-pfad', 301);
// Redirect-Tabelle im Admin für dynamische Verwaltung
```

## Audit-Checkliste

```
DISCOVERY: robots.txt dynamisch, sitemap mit hreflang, nur publizierte Inhalte
META: title+description auf jeder Seite, canonical, hreflang DE+EN+x-default
OG: og:type/title/description/image auf jeder Seite, Default-Bild vorhanden
JSON-LD: Organization+BreadcrumbList minimum, validiert
CONTENT: SEO-Felder auf allen Models, Alt-Texte, Heading-Hierarchie korrekt
REDIRECTS: Alte URLs → 301, keine Ketten, keine Schleifen
PERFORMANCE: Discovery Files gecacht, keine N+1 in Sitemap, <500ms Response
```
