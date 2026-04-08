---
name: init-project
description: "Richtet ein neues Projekt ein: Stack erkennen, .claude/ Ordner, Rules, Feature-Tracking, CLAUDE.md. Nutze bei: 'neues Projekt einrichten', 'Projekt initialisieren', 'init', 'Setup', 'Projekt starten'."
---

# /init-project – Projekt-Setup

Du richtest ein neues Projekt für die Zusammenarbeit ein. Stack erkennen, Struktur anlegen, Qualitätsstandards setzen.

## Workflow

### 1. Stack erkennen

```bash
# Was ist das für ein Projekt?
ls composer.json 2>/dev/null && echo "PHP_PROJECT=true"
ls artisan 2>/dev/null && echo "LARAVEL=true"
ls package.json 2>/dev/null && echo "NODE_PROJECT=true"
ls style.css functions.php 2>/dev/null && echo "WORDPRESS=true"
ls next.config.* 2>/dev/null && echo "NEXTJS=true"
ls nuxt.config.* 2>/dev/null && echo "NUXT=true"
ls tsconfig.json 2>/dev/null && echo "TYPESCRIPT=true"
ls tailwind.config.* 2>/dev/null && echo "TAILWIND=true"
ls docker-compose* Dockerfile 2>/dev/null && echo "DOCKER=true"
cat composer.json 2>/dev/null | grep -o '"filament\|"livewire\|"inertia' | head -5
cat package.json 2>/dev/null | grep -o '"react\|"vue\|"svelte\|"next\|"nuxt\|"astro' | head -5
```

### 2. User fragen

Stelle diese Fragen (nur was nicht aus dem Code erkennbar ist):

1. **Projektname?** (für CLAUDE.md Header)
2. **Was macht das Projekt?** (1-2 Sätze)
3. **Welche Sprachen?** (DE, EN, beide?)
4. **Gibt es ein Design-System?** (Preline, shadcn, Flowbite, custom?)
5. **Git-Workflow?** (main direkt, feature branches, PRs?)
6. **Besonderheiten?** (Multi-Tenant, API-only, Headless CMS, etc.)

### 3. Struktur anlegen

Erstelle im Projekt-Root:

```
.claude/
├── rules/           # Projekt-spezifische Rules
│   └── project.md   # Stack + Projekt-Konventionen
├── settings.json    # Permissions für dieses Projekt
features/
├── INDEX.md         # Feature-Tracking
```

Plus eine `CLAUDE.md` im Projekt-Root.

### 4. Dateien generieren

#### .claude/rules/project.md

```markdown
---
description: "Projekt-spezifische Regeln für {Projektname}"
globs: "**/*"
---

# {Projektname} – Projekt-Regeln

## Stack
- **Backend:** {Laravel 12 / WordPress 6.x / Next.js 15 / ...}
- **Frontend:** {Blade + Alpine / React + Tailwind / Bricks Builder / ...}
- **Admin:** {Filament v3 / wp-admin / Custom / ...}
- **DB:** {MySQL / MariaDB / PostgreSQL / Supabase / ...}
- **Queue:** {Redis + Horizon / Database / ...}
- **Payment:** {Mollie / Stripe / keins}

## Konventionen
- **Sprache Code:** Englisch
- **Sprache UI:** {DE / EN / DE+EN}
- **Git:** {main direkt / feature branches / PRs}
- **Tests:** {Pest / PHPUnit / Vitest / Playwright}

## Besonderheiten
{Multi-Tenant, DSGVO-kritisch, API-only, etc.}

## Wichtige Pfade
{Stack-abhängig generieren}
```

#### .claude/settings.json

Angepasst an den Stack:

**Laravel:**
```json
{
  "permissions": {
    "allow": [
      "Bash(php artisan *)",
      "Bash(composer *)",
      "Bash(npm run *)",
      "Bash(vendor/bin/pint *)",
      "Bash(vendor/bin/pest *)",
      "Bash(git *)",
      "Bash(ls *)",
      "Bash(find *)"
    ]
  }
}
```

**WordPress:**
```json
{
  "permissions": {
    "allow": [
      "Bash(wp *)",
      "Bash(composer *)",
      "Bash(npm run *)",
      "Bash(git *)",
      "Bash(ls *)",
      "Bash(find *)"
    ]
  }
}
```

**Node/Next.js:**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(git *)",
      "Bash(ls *)",
      "Bash(find *)"
    ]
  }
}
```

#### features/INDEX.md

```markdown
# Feature-Index – {Projektname}

| ID | Feature | Status | Spec | Erstellt |
|----|---------|--------|------|----------|

**Nächste ID:** FEAT-1

## Status-Legende
- **Planned** – Spec geschrieben, Architektur offen
- **Architected** – Technischer Entwurf fertig
- **In Progress** – Wird implementiert
- **In Review** – QA läuft
- **Done** – Getestet und deployed
```

#### CLAUDE.md (Projekt-Root)

Template je nach Stack:

**Laravel:**
```markdown
# CLAUDE.md – {Projektname}

## Projektübersicht
{Beschreibung}

## Stack
- Laravel {version}, Filament v3, Livewire, Tailwind CSS, Alpine.js
- DB: MariaDB | Queue: Redis + Horizon

## Dev-Workflow
\`\`\`bash
composer run dev          # Server + Vite + Horizon
composer run test         # Tests
vendor/bin/pint --dirty   # Code-Formatierung
\`\`\`

## Wichtige Regeln
- Feature-Workflow: /requirements → /architecture → /backend + /frontend → /qa → /deploy
- Feature-Tracking in features/INDEX.md
- Conventional Commits
- Tests vor jedem Merge
```

**WordPress:**
```markdown
# CLAUDE.md – {Projektname}

## Projektübersicht
{Beschreibung}

## Stack
- WordPress {version}, Child-Theme, {Bricks Builder / Elementor / Gutenberg}
- Plugins: {relevante Plugins}

## Regeln
- IMMER Child-Theme – nie Parent editieren
- Assets via wp_enqueue_script/style
- Übersetzbar: __(), _e(), esc_html__()
- Feature-Tracking in features/INDEX.md
```

**Next.js:**
```markdown
# CLAUDE.md – {Projektname}

## Projektübersicht
{Beschreibung}

## Stack
- Next.js {version}, TypeScript, Tailwind CSS, {shadcn/ui}
- DB: {Supabase / Prisma / ...}

## Dev-Workflow
\`\`\`bash
npm run dev              # Development
npm run build            # Production build
npm test                 # Tests
\`\`\`

## Regeln
- TypeScript strict mode
- shadcn/ui Components prüfen bevor neue erstellt werden
- Feature-Tracking in features/INDEX.md
```

### 5. Plugins & Erweiterungen prüfen

Prüfe welche Plugins installiert sind und empfehle fehlende:

```bash
# Installierte Plugins lesen
cat ~/.claude/settings.json | grep -o '"[a-z-]*@[a-z-]*"' | sort
```

**Erwartete Plugins (Christophs Standard-Setup):**

| Plugin | Zweck | Pflicht |
|---|---|---|
| `superpowers@superpowers-marketplace` | Brainstorming, Plans, Git Worktrees, Debugging, Code Review | Ja |
| `ui-ux-pro-max@ui-ux-pro-max-skill` | 50+ Design-Stile, Farben, Fonts, UX-Guidelines | Ja (Frontend) |
| `claude-mem@thedotmack` | Persistentes Gedächtnis über Sessions hinweg | Ja |
| `superpowers-chrome@superpowers-marketplace` | Browser-Steuerung via DevTools Protocol | Empfohlen |
| `feature-dev@claude-code-plugins` | Guided Feature Development | Empfohlen |
| `code-review@claude-code-plugins` | Pull Request Reviews | Empfohlen |
| `frontend-design@claude-code-plugins` | Production-grade Frontend Interfaces | Empfohlen (Frontend) |
| `elements-of-style@superpowers-marketplace` | Besseres technisches Schreiben | Nice-to-have |
| `superpowers-developing-for-claude-code@superpowers-marketplace` | Plugin-Entwicklung | Nur für Plugin-Dev |
| `plugin-dev@claude-code-plugins` | Plugin-Erstellung | Nur für Plugin-Dev |
| `security-guidance@claude-code-plugins` | Security-Patterns | Empfohlen |

**Fehlende Pflicht-Plugins melden:**
> Folgende Plugins fehlen und sollten installiert werden:
> ```bash
> claude plugins add superpowers@superpowers-marketplace
> claude plugins add ui-ux-pro-max@ui-ux-pro-max-skill
> claude plugins add claude-mem@thedotmack
> ```

**Bei Frontend-Projekten zusätzlich empfehlen (wenn nicht installiert):**
> Dieses Projekt hat Frontend-Komponenten. Empfohlene Plugins:
> ```bash
> claude plugins add frontend-design@claude-code-plugins
> claude plugins add superpowers-chrome@superpowers-marketplace
> ```

### 6. Stack-spezifische Extras

**Laravel-Projekte – zusätzlich erstellen:**
- Prüfe ob `app/Policies/` existiert → Hinweis wenn leer
- Prüfe ob `.env.example` existiert → Hinweis wenn nicht
- Prüfe ob Tests existieren → Hinweis wenn `tests/` leer

**WordPress-Projekte – zusätzlich erstellen:**
- `.claude/rules/wordpress.md` mit Bricks/Child-Theme Regeln
- Prüfe ob Child-Theme aktiv ist
- Prüfe ob `languages/` Ordner existiert

**Node-Projekte – zusätzlich erstellen:**
- Prüfe ob `tsconfig.json` strict ist
- Prüfe ob ESLint konfiguriert ist
- Prüfe ob `.env.local.example` existiert

### 7. Zusammenfassung zeigen

```markdown
## Projekt eingerichtet: {Name}

**Stack erkannt:** {Stack}
**Erstellt:**
- [x] .claude/rules/project.md
- [x] .claude/settings.json
- [x] features/INDEX.md
- [x] CLAUDE.md

**Nächster Schritt:**
→ `/requirements` um das erste Feature zu spezifizieren
→ `/help` für eine Übersicht aller verfügbaren Skills
```

## Regeln

1. **Nicht überschreiben**: Wenn CLAUDE.md oder .claude/ schon existiert → fragen ob ergänzen oder überspringen
2. **Minimal**: Nur das erstellen was der Stack braucht, kein Bloat
3. **User-Input**: Nicht raten – fragen wenn unklar
4. **Bestehende Konventionen respektieren**: Wenn das Projekt schon Patterns hat, diese übernehmen statt neue erfinden
