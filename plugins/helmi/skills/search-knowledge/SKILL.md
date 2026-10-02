---
name: search-knowledge
description: Finds information in the user's Helmi organization and explains what Helmi holds. Use when the user asks what we know about a topic, person, company or deal, asks to find something "in Helmi" or "in our docs", or asks what is available in Helmi (which modules, what is in the vault, what data exists).
---

# Searching Helmi

All tools are on the `helmi` MCP server bundled with this plugin. Everything is scoped to the user's current organization.

## Which tool

| The user wants | Call |
|---|---|
| any information question where the location is not explicit | `search-knowledge` first: one ranked query over documents, notes and meetings |
| a subject a passage names (a person, company, topic page) | `get-subject` |
| who a person or organization is | `search-entities`, or `resolve` for a name or email |
| text from documents only ("search the vault") | `search-documents`, then `documents-get` |
| notes only ("in my notes") | `list-notes`, then `get-note` |
| a meeting | `meetings-list`, then `meetings-get` |
| portfolio numbers | `get-portfolio-companies`, `get-metric-types`, `get-metrics` |
| what happened recently | `get-recent-activity`, `updates-list` |

## "What's available in Helmi"

Answer from the server, not from memory:
1. Read the resources `helmi://context/about-helmi`, `helmi://context/user`, `helmi://context/organization`.
2. Call `vault-overview` for vault stats, root folders and recent files.
3. List the modules: Documents (vault), Notes, Meetings, Email, Projects and Tasks, Portfolio, People and Organizations. Mention that email needs a connected inbox.

## Rules

- One search, then answer. Do not fan out every search tool at the same question.
- Cite where each fact came from (document, note, meeting, email).
- Empty result means say "Helmi has nothing on that". Do not fill the gap from general knowledge and present it as recorded.
