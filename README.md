# Claude Code Skills & Rules

> **I built a SaaS with 114 models, 157 services, and 421 views in 28 days. Solo. These are the skills and rules that made it possible.**

I'm a web developer from Austria. In March 2026, I started building [arkmetis](https://github.com/stoffl6781) – a SaaS platform for agencies that combines SEO monitoring, AI visibility tracking (GEO), accessibility audits, and an AI toolkit with 56 tools.

After **1,471 commits in 28 days**, I realized the bottleneck was never the coding. It was the *process*. Claude would write great code – but without structure, every session started from scratch. It would search for files, guess at conventions, miss edge cases, and forget what we discussed yesterday.

So I built a system: **19 skills that enforce a development workflow, 4 rules that auto-apply by file type, and a documentation pattern that saves thousands of tokens per session.**

The result: **~233,000 lines of production code** with 1,400 tests, full WCAG 2.1 AA compliance, DSGVO-conformity, and a billing system that handles subscriptions, lifetime licenses, and a free tier – all built by one person talking to Claude.

This repo is that system. Use it as-is, cherry-pick what you need, or fork it as a starting point for your own workflow.

**Stack Focus:** Laravel, WordPress, Tailwind CSS, Alpine.js, Vue/React
**Quality Standards:** WCAG 2.1 AA, DSGVO/GDPR, Security-first, A11y-first

## What's included

### Workflow Skills (development lifecycle)

| Skill | Trigger in chat | Purpose |
|---|---|---|
| **requirements** | "neues Feature", "spec schreiben" | Write feature specs with User Stories, Acceptance Criteria, Edge Cases |
| **architecture** | "wie bauen wir das", "Datenmodell" | Technical design BEFORE coding: Models, Services, Routes |
| **frontend** | "UI bauen", "responsive", "Dark Mode" | UI implementation with quality checklist (responsive, a11y, dark mode) |
| **backend** | "Service erstellen", "Migration" | Laravel/WP backend by spec: Models, Services, Controllers, Jobs |
| **qa** | "testen", "ist das sicher" | Testing + Security Audit + Bug documentation |
| **deploy** | "go live", "deployen" | Go-Live checklist (Laravel & WordPress) |
| **help** | "wo stehe ich", "was kommt als nächstes" | Show project status and recommended next step |

### Project Management Skills

| Skill | Trigger in chat | Purpose |
|---|---|---|
| **init-project** | "neues Projekt", "Setup" | Bootstrap new projects: detect stack, create structure, check plugins |
| **audit-project** | "Projekt prüfen", "was fehlt hier" | Analyze existing projects, score quality (0-100), identify gaps |
| **docs-structure** | "Doku anlegen", "wo finde ich was" | Hub-Pattern documentation with code paths and trigger words |

### Domain Skills (specialized audits)

| Skill | Trigger in chat | Purpose |
|---|---|---|
| **laravel-tests** | "Tests schreiben", "Coverage" | Generate Pest tests by priority (Critical → Useful) |
| **laravel-security-audit** | "Security Audit", "DSGVO-Check" | OWASP + DSGVO security audit with severity framework |
| **laravel-performance** | "Performance", "Seite ist langsam" | Performance audit (target: every page < 2 seconds) |
| **laravel-a11y** | "A11y prüfen", "Barrierefreiheit" | WCAG 2.1 AA accessibility audit for Blade/Livewire |
| **seo** | "SEO", "robots.txt", "sitemap" | Classical SEO: robots.txt, sitemap, meta tags, JSON-LD, hreflang |
| **geo** | "GEO", "KI-Auffindbarkeit", "ai.txt" | Generative Engine Optimization: ai.txt, llms.txt, AI crawler config |
| **laravel-docs** | "Dokumentation erstellen", "MkDocs" | Generate MkDocs documentation from Laravel codebase |
| **portfolio-texte** | "Portfolio-Text", "Case Study" | Write portfolio/case study texts for web projects |

### Utility Skills

| Skill | Trigger in chat | Purpose |
|---|---|---|
| **git-commit** | "commit", "push", "Änderungen sichern" | Smart git commit with Conventional Commits |

### Rules (auto-applied by file path)

| Rule | Applies to | Purpose |
|---|---|---|
| **General** | `**/*` | Code quality, naming, communication, git conventions |
| **Backend** | `app/**/*.php`, `routes/**`, `config/**` | PHP/Laravel/WordPress patterns, strict types, DI |
| **Frontend** | `resources/views/**`, `*.vue`, `*.tsx` | Tailwind, A11y, responsive, dark mode, component reuse |
| **Security** | `.env*`, `config/**`, `routes/**` | Secrets, CSRF, rate limiting, DSGVO, security headers |

## Installation

### Step 1: Copy the files

```bash
# Clone
git clone https://github.com/stoffl6781/claude-skill.git

# Copy skills to your Claude Code config
cp -r claude-skill/skills/* ~/.claude/skills/

# Copy rules
cp -r claude-skill/rules/* ~/.claude/rules/
```

Or cherry-pick what you need:

```bash
# Just the workflow pipeline
cp -r claude-skill/skills/{requirements,architecture,frontend,backend,qa,deploy,help} ~/.claude/skills/

# Just the audit skills
cp -r claude-skill/skills/{laravel-security-audit,laravel-performance,laravel-a11y} ~/.claude/skills/

# Just the rules
cp -r claude-skill/rules/* ~/.claude/rules/
```

### Step 2: Restart Claude Code

Close and reopen Claude Code (or start a new conversation). Skills are loaded when a session starts.

### Step 3: Verify

In the Claude Code chat, type `/` – you should see your skills in the autocomplete list:

```
/help
/requirements
/architecture
/frontend
/backend
/qa
/deploy
...
```

## How to use

### Important: Skills are chat commands, not terminal commands

Skills are **slash commands inside the Claude Code chat** – not terminal commands. You type them in the conversation with Claude, not in your shell.

**In Claude Code chat:**
```
You: /help
→ Claude loads the skill and shows your project status + next steps

You: /requirements
→ Claude walks you through writing a feature spec

You: Can you check if this is secure?
→ Claude recognizes the intent and loads /laravel-security-audit automatically
```

**This does NOT work:**
```bash
# These are NOT terminal commands
$ /help          # ✗ Won't work in your terminal
$ claude help    # ✗ Not a CLI command
```

### Three ways to trigger a skill

1. **Directly** – Type the slash command in chat:
   ```
   You: /qa
   ```

2. **By asking** – Claude recognizes keywords from the skill description and loads it automatically:
   ```
   You: "Is this feature secure?"
   → Claude loads /laravel-security-audit

   You: "What should I do next?"
   → Claude loads /help

   You: "I need to add a new feature for user notifications"
   → Claude loads /requirements
   ```

3. **In combination** – Use skills as part of a conversation:
   ```
   You: "I just finished the payment integration. /qa"
   → Claude tests the payment feature against its acceptance criteria
   ```

### Rules work automatically

Unlike skills, **rules don't need to be invoked**. They apply automatically based on which files Claude is working on:

- Editing `app/Services/BillingService.php` → `backend.md` rules are active (strict types, DI, no raw SQL)
- Editing `resources/views/billing/index.blade.php` → `frontend.md` rules are active (Tailwind, a11y, responsive)
- Editing `.env.example` → `security.md` rules are active (no secrets, document all vars)
- `general.md` is **always** active (code quality, naming, git conventions)

## Recommended Development Workflow

```
/requirements  →  /architecture  →  /frontend + /backend  →  /qa  →  /deploy
     ↑                                                          │
     └──────────── fix bugs, then re-test ──────────────────────┘
```

1. **`/requirements`** – Define what to build (User Stories, AC, Edge Cases)
2. **`/architecture`** – Plan how to build it (Models, Services, Routes)
3. **`/frontend`** + **`/backend`** – Build it (with quality checklists)
4. **`/qa`** – Test it (functional, security, a11y, regression)
5. **`/deploy`** – Ship it (pre-flight checklist, post-deployment verification)

Use **`/help`** anytime to see where you are and what comes next.

## Testing Philosophy – How We Prevent 500 Errors

When you build fast with AI, you break things fast too. A missing `@endforeach` in a Blade view. A refactored service that silently stops working. An authorization check that got lost during a controller rewrite.

These skills enforce a **7-layer testing approach** that catches bugs before they reach production:

### The testing pyramid

```
Layer 7:  Deployment Checks          /deploy pre-flight
Layer 6:  Regression                 Full test suite before every commit
Layer 5:  Security                   Auth bypass, CSRF, injection, rate limiting
Layer 4:  Integration                Controller → Service → DB round-trips
Layer 3:  Business Logic             Services in isolation
Layer 2:  Data Integrity             Models, relations, scopes, casts
Layer 1:  Infrastructure             Jobs, mail, commands, enums
```

### What each layer catches

| Layer | What it prevents |
|---|---|
| **Services** (Unit) | Wrong calculations, broken business logic, edge cases |
| **Models** (Unit) | Broken relations, wrong casts, missing scopes |
| **Policies** (Unit) | Authorization holes – User A sees User B's data |
| **Jobs** (Unit) | Queue failures that silently block background processing |
| **Controllers** (Feature) | HTTP 500 errors on pages with missing or empty data |
| **Security** (Feature) | Auth bypass, CSRF, IDOR, rate limiting gaps |
| **Blade parsing** | Template errors that crash every page using that layout |
| **Mail** (Unit) | Email failures from missing relations or null values |

### The kind of bugs this catches

These are **real patterns** that automated tests prevent:

- **Authorization gap:** A refactored controller loses its `$this->authorize()` call → any logged-in user can see any record. Policy tests catch this instantly.
- **Billing logic error:** A downgrade flow doesn't validate limits → users keep premium features on a free plan. Business logic tests prevent this.
- **Blade parse error:** An `@json()` with invalid content causes a 500 on every page that uses the layout. `php artisan view:cache` in the test routine catches it before commit.
- **Queue failure:** A job divides by zero on empty datasets → gets stuck "running" forever. Job tests verify edge cases.
- **Data inflation:** A detection algorithm counts duplicates → metrics are inflated by 30%. Unit tests with known inputs verify exact outputs.

### How testing fits into the skill workflow

```
/requirements  →  Acceptance Criteria define WHAT to test
/architecture  →  Service boundaries define WHERE to test
/backend       →  Quality checklist: "No dd(), strict types, authorize()"
/frontend      →  Checklist: "Responsive, a11y, dark mode, empty states"
/qa            →  Tests every AC + security audit + regression
/deploy        →  Test suite must be green before deploy
```

The `/qa` skill generates tests by priority:

| Priority | What | Example |
|---|---|---|
| **Critical** | Auth, billing, data isolation | *"User cannot access other team's data"* |
| **High** | CRUD, business logic, API | *"Creating a record deducts credits correctly"* |
| **Medium** | Validation, edge cases, mail | *"Empty input doesn't crash the processor"* |
| **Useful** | UI components, admin pages | *"Admin dashboard loads without errors"* |

**The rule is simple: If it's not tested, it's not shipped.**

### Beyond code: Visual testing with Superpowers Chrome

Not everything can be caught by unit tests. A button might pass all assertions but be invisible because of a z-index issue. A modal might work perfectly in tests but overlap the navigation on mobile. A CSS variable might render as `undefined` in dark mode.

That's where the **superpowers-chrome** plugin comes in. It opens a real Chrome browser via DevTools Protocol and lets Claude **see what the user sees**:

```
You: "Check if the billing page looks correct in dark mode."

Claude: *opens Chrome → navigates to the page → switches to dark mode
→ takes screenshot → analyzes the visual output*

"The cards have white text on a light background in dark mode.
The CSS variable --color-surface isn't applied to the card component.
Fix: Add .dark class to the card wrapper."
```

We use this for:

- **Visual regression** – Does the page still look right after a CSS refactor?
- **Dark mode verification** – Contrast issues that no unit test can catch
- **Responsive checks** – Does the layout break on specific viewport widths?
- **Real browser behavior** – JavaScript that only fails in actual Chrome (not in test environments)

### Cross-stack testing

The same testing approach works across very different stacks:

- **Chrome Extensions** – Content scripts, popup UI, cross-origin messaging. Superpowers Chrome lets Claude interact with the extension in a real browser, test element positioning, and verify the relay architecture actually works.

- **CodeIgniter / Legacy PHP** – The `/qa` skill adapts: instead of Pest, it generates PHPUnit tests. Instead of Eloquent, it tests raw query builder calls. The security checklist catches the same issues regardless of framework.

- **MCP Server Development** – Testing MCP tools requires real API calls. Superpowers Chrome verifies OAuth flows work end-to-end in a browser, not just in mocked tests.

- **Python / Desktop Apps** – The workflow skills (`/requirements` → `/architecture` → `/qa`) provide structure for any stack. The testing layer adapts: pytest instead of Pest, but the same priority system.

### Local-first: Testing with Laravel Herd

We never test against production. Everything runs locally on [Laravel Herd](https://herd.laravel.com) – a zero-config dev environment for macOS that gives you PHP, Nginx, Redis, and automatic `.test` domains. Database via [DBngin](https://dbngin.com) (MariaDB).

```
Laravel Herd (PHP 8.4, Nginx) + DBngin (MariaDB 10.11)
├── myapp.test             → Laravel SaaS
├── crm.test               → CodeIgniter CRM
├── client.test            → WordPress + Bricks
└── internal.test          → Laravel internal tool
```

**Why this matters:**

- **Real database testing** – Tests run against MariaDB, not SQLite. DB-specific issues (JSON columns, fulltext indexes, foreign key cascades) get caught locally.
- **One-command dev setup** – `composer run dev` starts Server + Queue Worker + Vite + Log Viewer via `concurrently`.
- **Automatic HTTPS** – SSL locally means mixed content issues, secure cookies, and HSTS are verified before deploy.
- **Multi-project** – Switch between Laravel, WordPress, and CodeIgniter instantly. Same DB server, same Redis, same PHP.
- **View cache as safety net** – `php artisan view:cache` before every commit catches Blade parse errors. This single command prevents more 500 errors than any other test.

```bash
# Pre-commit routine (enforced by /deploy)
php artisan view:cache          # Blade parse errors?
php artisan test --parallel     # Full test suite green?
vendor/bin/pint --dirty         # Code style clean?
# Only then: git commit
```

The skills don't care about your stack. They care about **process and quality**. The testing layer adapts to whatever framework you're in – what stays constant is: **test before you ship**.

## Documentation Structure (`/docs-structure`) – Save Tokens, Ship Faster

The biggest hidden cost in AI-assisted development is **context**. Every time Claude opens a new session, it doesn't know where your files are. It searches, reads, guesses – burning tokens and time.

The `/docs-structure` skill solves this with a **Hub-Pattern**:

```
docs/
├── patterns/
│   ├── development.md          # Global dev rules
│   └── doc-template.md         # Template for new modules
├── auth/
│   └── general.md              # Hub: Auth module
├── billing/
│   └── general.md              # Hub: Billing module
├── seo/
│   └── general.md              # Hub: SEO module
└── {feature}/
    └── general.md              # Hub: Any module
```

### What's in a Hub file?

Each `general.md` contains everything Claude needs to work on that module – **without scanning the codebase**:

```markdown
## Code-Pfade
| Typ        | Pfad                                          |
|------------|-----------------------------------------------|
| Controller | `app/Http/Controllers/Billing/BillingController.php` |
| Service    | `app/Services/Billing/BillingService.php`      |
| Model      | `app/Models/Subscription.php`                  |
| Views      | `resources/views/billing/`                     |
| Routes     | `routes/web.php:L320-L345`                     |
| Tests      | `tests/Feature/Billing/BillingTest.php`        |

## Relevante Enums
| Enum               | Werte                              |
|--------------------|------------------------------------|
| `SubscriptionPlan` | starter, professional, business    |
| `BillingMode`      | free, subscription, lifetime       |
```

### How it saves tokens

| Without Hub-Pattern | With Hub-Pattern |
|---|---|
| Claude runs `find`, `grep`, `ls` across the entire codebase | Claude reads one 50-line file |
| 5-10 tool calls just to locate files | 1 tool call → knows everything |
| ~2,000-5,000 tokens wasted on exploration | ~200 tokens for the hub file |
| Guesses wrong paths, retries | Exact paths, no guessing |
| Every new session starts from zero | Every session starts informed |

**On a project with 100+ files, this saves 3,000-8,000 tokens per task** – that's 20-40% of a typical interaction.

### The Trigger-Word system

In your project's `CLAUDE.md`, you add a lookup table:

```markdown
## Dokumentation

| Bereich  | Hub-Datei                    | Trigger-Wörter                        |
|----------|------------------------------|---------------------------------------|
| SEO      | `docs/seo/general.md`        | SEO, PageSpeed, Crawler, Sitemap      |
| Billing  | `docs/billing/general.md`    | Zahlung, Abo, Subscription, Mollie    |
| Auth     | `docs/auth/general.md`       | Login, Register, Passwort, 2FA        |
| A11y     | `docs/a11y/general.md`       | Barrierefreiheit, WCAG, Audit         |
```

When you say *"Fix the billing webhook"*, Claude matches "billing" → reads `docs/billing/general.md` → knows exactly where `BillingService.php`, `MollieWebhookService.php`, and `BillingController.php` live → starts working immediately.

### Auto-Update rules

The pattern stays accurate because of built-in rules:

1. **Move/rename a file** → Update the Code-Pfade table
2. **Add a new enum** → Update the Enum table
3. **Change a scheduled task** → Update the Tasks table
4. **Finish a feature** → Update status (⬚ → 🔄 → ✅)

Run `/docs-structure update` after major changes to verify all paths are still correct.

### When to use it

- **`/docs-structure init`** – Set up the full structure for an existing project
- **`/docs-structure billing`** – Document a specific module
- **`/docs-structure update`** – Verify and refresh all hub files after changes

This pattern was developed on [arkmetis](https://github.com/stoffl6781) (1,400+ commits, 157 services, 421 views) and proved essential for maintaining velocity at scale.

## Feature Tracking

Skills use `features/INDEX.md` for tracking feature status:

```
Planned → Architected → In Progress → In Review → Done
```

Run `/init-project` to set up the tracking structure automatically.

## Recommended Plugins

The `/init-project` and `/audit-project` skills check for these plugins:

| Plugin | Purpose | Required | Repository |
|---|---|---|---|
| `superpowers@superpowers-marketplace` | Brainstorming, Plans, Debugging, Code Review | Yes | [obra/superpowers](https://github.com/obra/superpowers) |
| `ui-ux-pro-max@ui-ux-pro-max-skill` | Design intelligence (50+ styles, 161 palettes, 57 fonts) | Yes (frontend) | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| `claude-mem@thedotmack` | Persistent memory across sessions | Yes | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) |
| `frontend-design@claude-code-plugins` | Production-grade UI generation | Recommended | [anthropics/claude-code](https://github.com/anthropics/claude-code) (built-in) |
| `superpowers-chrome@superpowers-marketplace` | Browser control via DevTools Protocol | Recommended | [anthropics/superpowers-chrome](https://github.com/anthropics/superpowers-chrome) |
| `code-review@claude-code-plugins` | Pull request reviews | Recommended | [anthropics/claude-code](https://github.com/anthropics/claude-code) (built-in) |
| `elements-of-style@superpowers-marketplace` | Better technical writing | Nice-to-have | [superpowers-marketplace](https://github.com/obra/superpowers-marketplace) |
| `security-guidance@claude-code-plugins` | Security patterns | Recommended | [anthropics/claude-code](https://github.com/anthropics/claude-code) (built-in) |

### How to install plugins

Plugins come from **marketplaces** (GitHub repositories that host plugin collections). You need to add the marketplace first, then enable the plugin.

**Step 1: Add marketplaces** (one-time setup)

Claude Code's built-in plugins (`@claude-code-plugins`) are available by default. For third-party plugins, you need to add their marketplace:

Open Claude Code settings (`~/.claude/settings.json`) and add the marketplaces under `extraKnownMarketplaces`:

```json
{
  "extraKnownMarketplaces": {
    "superpowers-marketplace": {
      "source": { "source": "github", "repo": "obra/superpowers-marketplace" }
    },
    "thedotmack": {
      "source": { "source": "github", "repo": "thedotmack/claude-mem" }
    },
    "ui-ux-pro-max-skill": {
      "source": { "source": "github", "repo": "nextlevelbuilder/ui-ux-pro-max-skill" }
    }
  }
}
```

**Step 2: Enable plugins**

Add the plugins to `enabledPlugins` in the same `settings.json`:

```json
{
  "enabledPlugins": {
    "superpowers@superpowers-marketplace": true,
    "ui-ux-pro-max@ui-ux-pro-max-skill": true,
    "claude-mem@thedotmack": true,
    "frontend-design@claude-code-plugins": true,
    "superpowers-chrome@superpowers-marketplace": true,
    "code-review@claude-code-plugins": true,
    "elements-of-style@superpowers-marketplace": true,
    "security-guidance@claude-code-plugins": true
  }
}
```

**Step 3: Restart Claude Code**

Close and reopen Claude Code (or start a new session). The plugins will be downloaded and activated automatically.

**Step 4: Verify**

In Claude Code, type `/` and you should see the plugin skills (e.g., `superpowers:brainstorming`, `ui-ux-pro-max:ui-ux-pro-max`, `claude-mem:mem-search`).

### Full settings.json example

Here's a complete `~/.claude/settings.json` with all marketplaces and plugins:

```json
{
  "permissions": {
    "allow": []
  },
  "enabledPlugins": {
    "superpowers@superpowers-marketplace": true,
    "ui-ux-pro-max@ui-ux-pro-max-skill": true,
    "claude-mem@thedotmack": true,
    "frontend-design@claude-code-plugins": true,
    "superpowers-chrome@superpowers-marketplace": true,
    "code-review@claude-code-plugins": true,
    "feature-dev@claude-code-plugins": true,
    "security-guidance@claude-code-plugins": true,
    "elements-of-style@superpowers-marketplace": true,
    "superpowers-developing-for-claude-code@superpowers-marketplace": true
  },
  "extraKnownMarketplaces": {
    "claude-code-plugins": {
      "source": { "source": "github", "repo": "anthropics/claude-code" }
    },
    "superpowers-marketplace": {
      "source": { "source": "github", "repo": "obra/superpowers-marketplace" }
    },
    "thedotmack": {
      "source": { "source": "github", "repo": "thedotmack/claude-mem" }
    },
    "ui-ux-pro-max-skill": {
      "source": { "source": "github", "repo": "nextlevelbuilder/ui-ux-pro-max-skill" }
    }
  }
}
```

## Language

- Skills and rules are in **German** (optimized for DACH market)
- Code comments and git messages are in **English**
- Easily adaptable to English – the structure works in any language

## Stack Support

| Stack | Supported | Skills that adapt |
|---|---|---|
| **Laravel** | Full support | All skills |
| **WordPress** | Full support | `/frontend`, `/backend`, `/deploy`, `/seo`, `/geo` |
| **Next.js / Vue / React** | Supported | `/frontend`, `/backend`, `/qa`, `/deploy` |
| **Any PHP project** | Basic support | `/backend`, `/qa`, `/deploy` |

## Real-World Examples

### Example 1: Building a new feature from scratch

You want to add a "Client Portal" to your Laravel app where clients can view their project reports.

```
You: "I need a client portal where clients can log in and see their reports."

/requirements
→ Creates features/FEAT-12-client-portal.md with:
  - User Stories: "As a client, I want to see my project reports without needing a full account"
  - Acceptance Criteria: Login via magic link, read-only access, only own projects visible
  - Edge Cases: What if the client has multiple projects? What if a report is still generating?

/architecture
→ Reads the spec, asks 3 questions, then adds to FEAT-12:
  - Model: ClientAccess (email, project_id, token, expires_at)
  - Service: ClientPortalService (generateMagicLink, validateAccess, getReports)
  - Controller: ClientPortalController (login, dashboard, viewReport)
  - Views: client-portal/login.blade.php, dashboard.blade.php, report.blade.php
  - No new migrations needed – reuses existing Report model

/backend
→ Reads spec + architecture, creates:
  - Migration, Model with relations, Service with business logic
  - Controller with authorize() calls, Form Request for validation
  - Checks the quality checklist: strict types, no N+1, rate limiting on magic link

/frontend
→ Reads spec, checks existing components, builds:
  - Login page (centered card, magic link input)
  - Dashboard (project cards with report list)
  - Report viewer (PDF embed + download)
  - Checks: responsive, dark mode, a11y, loading states

/qa
→ Tests against every AC:
  - [x] Client can log in via magic link
  - [x] Client only sees own projects (tested with 2 clients)
  - [x] Magic link expires after 24h
  - Security: [x] Cannot guess other client tokens, [x] Rate limited
  - Writes 8 Pest tests

/deploy
→ Pre-flight checklist, then deploys
```

Total time: ~2 hours for a complete, tested, secure feature.

### Example 2: Taking over an existing project

A client hands you a WordPress site that "needs some work". You open it in Claude Code:

```
You: "I just inherited this WordPress project. What's the state?"

/audit-project
→ Scans the codebase, returns:

  Project Audit: Mueller Dental Website
  Stack: WordPress 6.4, Bricks Builder, Child-Theme
  Score: 42/100

  A) Project Structure     ❌  12/15  (no CLAUDE.md, no .claude/)
  B) Code Quality          ⚠️   8/15  (3x var_dump found, mixed tabs/spaces)
  C) Security              ❌   6/20  (no rate limiting, admin uses "admin123")
  D) Testing               ❌   0/15  (zero tests)
  E) Frontend / A11y       ⚠️   7/15  (missing alt texts, no skip-link)
  F) Internationalization  ⚠️   3/5   (hardcoded German strings in templates)
  G) Deployment-Ready      ❌   3/10  (WP_DEBUG=true in production!)
  H) Documentation         ❌   0/5   (no readme, no docs)
  I) Plugins               ⚠️   3/5   (superpowers missing)

  Critical: WP_DEBUG=true in production, no rate limiting, weak admin password
  Action Plan:
  1. /init-project → Create .claude/ structure          (15 min)
  2. /laravel-security-audit → Fix critical security    (30 min)
  3. /laravel-a11y → Fix accessibility issues            (1 hour)
  4. /docs-structure → Document the codebase             (30 min)

You: "Fix the critical security issues first."
→ Claude fixes WP_DEBUG, adds rate limiting, flags the weak password
```

### Example 3: Scaling a project with the Hub-Pattern

Your project has grown to 80+ models and you keep losing time because Claude searches for files every session.

```
You: "I can't keep explaining where everything is. Set up the docs structure."

/docs-structure init
→ Scans the codebase, identifies 12 modules, creates:

  docs/
  ├── patterns/development.md       # Dev rules
  ├── auth/general.md               # Controllers, Models, Routes for auth
  ├── billing/general.md            # Subscription, Mollie, Credits
  ├── seo/general.md                # Crawler, Audits, PageSpeed
  ├── geo/general.md                # AI Visibility, Mentions, Competitors
  ├── a11y/general.md               # WCAG Audit, Compliance
  ├── tools/general.md              # AI Toolkit, 56 tools
  ├── reports/general.md            # PDF, Alerts, Digests
  └── ... (4 more)

  Updated CLAUDE.md with lookup table:
  | Bereich | Hub-Datei | Trigger-Wörter |
  |---------|-----------|----------------|
  | Billing | docs/billing/general.md | Zahlung, Abo, Mollie, Credits |
  | SEO     | docs/seo/general.md     | Crawler, PageSpeed, Sitemap   |
  | ...     | ...                     | ...                           |

Next session:

You: "The Mollie webhook is failing on recurring payments."

Claude: *reads CLAUDE.md → matches "Mollie" → reads docs/billing/general.md
→ knows BillingService.php is at app/Services/Billing/BillingService.php
→ knows MollieWebhookService.php handles webhooks
→ knows the route is at routes/web.php:L340
→ opens the right file immediately, no searching*
```

Before the Hub-Pattern: 5-10 minutes of "let me find the files..." per session.
After: Claude starts working in seconds.

---

## Author

**Christoph Purin** – Web Developer, A11y Expert, Laravel & WordPress Specialist

- Website: [purin.at](https://www.purin.at)
- GitHub: [@stoffl6781](https://github.com/stoffl6781)

Built with [Claude Code](https://claude.ai/claude-code) and lots of coffee from Tyrol.

## License

MIT
