---
description: Orient Claude when working with Helmi data. Use whenever the user asks about their organization's documents, files, data room, contacts (people & organizations), meetings, transcripts, notes, email, portfolio companies, or metrics — anything that lives in Helmi. Points Claude at the connector as the source of truth and its own server-side guides.
---

# Using Helmi

Helmi is this organization's platform for its documents, contacts (people and
organizations), meetings, notes, email, and portfolio data. The **Helmi MCP
connector** is the authoritative, live source for all of it — prefer it over
assumptions or stale context.

## How to work with Helmi

1. **Let the server orient you.** The Helmi connector ships its own current
   guidance as MCP resources — an "about", "user", and "organization" context,
   plus a per-module overview and a workflows guide. Before non-trivial work,
   read the relevant ones and follow them. They are maintained server-side and
   are always up to date, so trust them over anything hardcoded here.
2. **Use the connector's tools** to search, read, and act on Helmi data instead
   of guessing. All IDs are UUIDs and everything is scoped to the current
   organization.
3. **First use triggers a one-time browser sign-in.** The connector uses OAuth;
   approve the prompt once and org-scoped access persists.

Keep this skill thin: detailed, evolving guidance lives in the connector's own
resources, not in this file.
