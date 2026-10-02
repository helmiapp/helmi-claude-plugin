# Helmi for Claude

A one-step way to connect Claude to your **Helmi** workspace — documents, contacts
(people & organizations), meetings, transcripts, notes, email, and portfolio data.

Instead of pasting a connector URL by hand, you add the Helmi marketplace once and
install the **Helmi** plugin. The plugin wires up the Helmi remote MCP connector and
signs you in with a one-time browser approval.

## What's inside

- A reference to the Helmi **remote MCP connector** (`https://api.sigma.helmigroup.com/v1/mcp/all`).
- An orientation skill (`using-helmi`) that points Claude at the connector's own guidance.
- Routing skills that tell Claude which Helmi tool answers which request: `search-knowledge`,
  `email`, `projects`, `documents`, `tasks`. Detailed tool behavior stays on the server
  (tool descriptions and connector resources), so it updates with each Helmi deploy.
- Two commands: `/helmi:wrap-up` proposes notes, vault files and tasks from the session and
  saves only what you approve; `/helmi:save <path>` files one document into the vault.
- Two hooks (Claude Code and Cowork only; claude.ai chat ignores hooks):
  - **End of session:** once per session, and only if files were written, Claude offers
    to save decisions and documents to Helmi. Nothing is written without your yes.
  - **Document written:** when Claude creates a new document (`.md`, `.pdf`, `.docx`,
    `.pptx`, `.xlsx`, `.csv`, over 1.5 KB, outside code folders), it suggests one vault
    location. At most twice per session. Hooks need `python3`.

Run `./test.sh` to check the hook scripts.

There are **no secrets or tokens** in this plugin. Access is granted per-user through
standard OAuth at first use; the Helmi server issues an org-scoped token after you
approve the browser sign-in.

## Requirements

- A **paid Claude plan** (Pro, Max, Team, or Enterprise). Plugins are not available on
  the Free plan.
- A **Helmi account** in the organization you want to connect to.
- A **one-time OAuth sign-in**: the first time Claude uses a Helmi tool, it opens a
  browser window for you to approve access. This cannot be skipped.

## Install — Claude Desktop / claude.ai (web)

1. Open **Settings → Plugins**.
2. Choose **Add → Add marketplace** and paste this repository's URL:
   ```
   https://github.com/helmiapp/helmi-claude-plugin
   ```
3. Find **Helmi** in the marketplace and click **Install**.
4. Start using it. The first Helmi request opens a browser window — **approve the
   OAuth sign-in** to grant access to your organization's data.

## Install — Claude Code (CLI)

```shell
# 1. Add the Helmi marketplace (once)
/plugin marketplace add https://github.com/helmiapp/helmi-claude-plugin.git

# 2. Install the plugin
/plugin install helmi@helmi-plugins

# 3. Activate it in the current session
/reload-plugins
```

> The `helmiapp/helmi-claude-plugin` shorthand also works, but it clones over
> **SSH** — use it only if you have a GitHub SSH key set up. The HTTPS `.git`
> URL above needs no credentials for this public repo, so it's the easiest path.

The first time Claude calls a Helmi tool it will flag the connector for sign-in. Run
`/mcp` and complete the **OAuth** flow (or `claude mcp login helmi`). After that,
access persists.

> Testing locally before this repo is published? Point the marketplace at a local path
> instead of the GitHub shorthand:
> ```shell
> /plugin marketplace add /absolute/path/to/helmi-claude-plugin
> /plugin install helmi@helmi-plugins
> ```

## Org-wide distribution (Team / Enterprise)

Admins can push Helmi to everyone in the organization so members get it — and its
updates — automatically, without each person adding the marketplace by hand. In your
organization's **managed settings** (`managed-settings.json`), register the marketplace
and enable the plugin by default:

```json
{
  "extraKnownMarketplaces": {
    "helmi-plugins": {
      "source": {
        "source": "github",
        "repo": "helmiapp/helmi-claude-plugin"
      },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "helmi@helmi-plugins": true
  }
}
```

- `enabledPlugins` marks the plugin **installed by default** for members.
- `autoUpdate: true` keeps the marketplace and plugin current in the background
  (third-party marketplaces have auto-update **off** by default otherwise).
- Each member still completes their **own** one-time OAuth sign-in — the plugin never
  carries anyone's credentials.

## Updating

Because the plugin is a thin reference, the connector's tools and guidance improve
**server-side** with each Helmi deploy — no action needed. You only need a plugin update
for rare structural changes, which ship as a `version` bump in `plugins/helmi/.claude-plugin/plugin.json`.

## Repository layout

```
helmi-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json          # marketplace catalog (lists the "helmi" plugin)
├── plugins/
│   └── helmi/
│       ├── .claude-plugin/
│       │   └── plugin.json        # plugin manifest
│       ├── .mcp.json              # remote MCP connector reference (OAuth, no secrets)
│       └── skills/
│           └── using-helmi/
│               └── SKILL.md       # thin orientation skill
└── README.md
```
