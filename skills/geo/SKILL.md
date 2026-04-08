---
name: geo
description: >
  GEO (Generative Engine Optimization) – KI-Auffindbarkeit für Laravel.
  Prüft: ai.txt, llms.txt, llms-full.txt, KI-Crawler in robots.txt,
  Content-Struktur für KI-Systeme.
  Nutze bei: "GEO", "KI-Auffindbarkeit", "ai.txt", "llms.txt",
  "wird das von KI gefunden", "Discovery Files", "LLM Discovery",
  "KI-Crawler", "GPTBot", "KI zitiert uns nicht", "KI-Indexierung".
  Für klassisches SEO → SEO Skill.
---

# GEO – Generative Engine Optimization

KI-Auffindbarkeit für ChatGPT, Claude, Perplexity, Gemini.
Für klassisches SEO → **SEO Skill**. GEO und SEO gehören zusammen.

## Workflow

| Schritt | Prüfen |
|---|---|
| 1. Analyse | Discovery Files vorhanden? Dynamisch? KI-Crawler erlaubt? |
| 2. Discovery Files | ai.txt, llms.txt, llms-full.txt erstellen/prüfen |
| 3. robots.txt | KI-Crawler explizit erlauben |
| 4. Content | Fakten-Blöcke, Entitäten-Verknüpfung, FAQ-Paare |
| 5. Filament | GEO-Einstellungen, Discovery-Status-Widget |

## ai.txt (site-agent.ai Format, Cache 24h)

```
Route: GET /ai.txt
Pflichtfelder: Allow-AI-Training: No, Allow-AI-Summarization: Yes,
  Allow-AI-Citation: Yes, Citation-Format, Llms-Txt, Sitemap,
  Contact, Content-Types, Primary-Language, Last-Updated (dynamisch)
```

## llms.txt (Markdown, llmstxt.org, Cache 24h)

```
Route: GET /llms.txt
Inhalt: Kurzbeschreibung, Statistiken (dynamisch aus DB),
  Kategorien-Liste, Wichtige Seiten (Links), Verweis auf llms-full.txt
```

## llms-full.txt (Vollständiger Katalog, Cache 12h)

```
Route: GET /llms-full.txt
Inhalt: ALLE publizierten Inhalte mit Metadaten (URL, Kategorie, Preis,
  Kurzbeschreibung). Max ~2000 Zeilen. Nur Excerpts, nicht vollen Content.
```

### Mehrsprachig

- ai.txt: Englisch (Standard)
- llms.txt / llms-full.txt: Hauptsprache (DE), optional separate EN-Version
- robots.txt: Referenz zu allen Discovery Files

## KI-Crawler in robots.txt

Diese User-Agents explizit erlauben (`Allow: /`):

| Crawler | Betreiber |
|---|---|
| GPTBot, ChatGPT-User | OpenAI |
| Google-Extended | Google/Gemini |
| Claude-Web, anthropic-ai | Anthropic |
| PerplexityBot | Perplexity |
| Applebot-Extended | Apple Intelligence |
| meta-externalagent, FacebookBot | Meta |
| CCBot | Common Crawl |
| Bytespider | ByteDance |

Zusätzlich in robots.txt: `Llms-txt: {URL}/llms.txt` und `Ai-txt: {URL}/ai.txt`

**Neue Crawler entdecken:** https://darkvisitors.com/agents, Server-Logs

## Content-Struktur für KI

- **Fakten-Blöcke:** Strukturierte Daten statt Fließtext (Preis, Dauer, Ort als Datenpunkte)
- **Entitäten:** Produkt → Kategorie → Region/Ort → Anbieter verknüpfen
- **FAQ:** Frage-Antwort-Paare (auch als JSON-LD → SEO Skill)
- **Autorität:** Impressum, Veröffentlichungsdatum, Aktualisierungsdatum
- **Aktualität signalisieren:** Last-Updated in ai.txt, lastmod in Sitemap, dateModified in JSON-LD

## Filament GEO-Einstellungen

```
geo_allow_ai_crawlers     Toggle (Default: true)
geo_allow_ai_citation     Toggle (Default: true)
geo_allow_ai_training     Toggle (Default: false)
geo_contact_email         Kontakt für KI-Anfragen

GeoDiscoveryWidget: Status aller Discovery Files + Crawler-Count
```

## Audit-Checkliste

```
FILES: ai.txt (site-agent.ai), llms.txt (dynamisch), llms-full.txt (alle Inhalte)
CRAWLER: robots.txt erlaubt alle bekannten KI-Crawler, Liste aktuell
CONTENT: Fakten-Blöcke, Entitäten verknüpft, FAQ vorhanden, Aktualität erkennbar
CACHE: ai.txt 24h, llms.txt 24h, llms-full.txt 12h, invalidiert bei Content-Änderung
FILAMENT: GEO-Settings konfigurierbar, Discovery-Status sichtbar
```
