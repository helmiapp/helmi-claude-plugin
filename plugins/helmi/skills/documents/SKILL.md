---
name: documents
description: Works with files in the Helmi vault. Use when the user asks to find, open, read, browse, share or download a document, asks what is in the vault or a folder, or asks to save, upload or update a file in Helmi.
---

# Documents in the Helmi vault

## Reading

| The user wants | Call |
|---|---|
| orientation ("what's in my vault") | `vault-overview`, then `browse-vault` with a `path` it surfaced |
| a document by topic or content | `search-documents`, then `documents-get` |
| a document by folder or filename | `browse-vault` |
| a download or share link | `get-download-link`; sharing analytics via `get-sharing-analytics` |
| older versions | `get-version-history` |

## Writing

`upload-vault-file` is the default for writing any file:
- **Text** (md, txt, csv, json, html): one call, `action: create` (or `update` to overwrite) with `path` and `content`. Up to 5 MB.
- **Binary** (pdf, docx, pptx, xlsx, images) or over 5 MB: `action: request-upload` with `path` and `sizeBytes`, run the returned curl against the local file, then `action: commit-upload` with the `uploadId`. Never base64 a binary into `content`.
- Pass `createParents: true` when the folder may not exist.
- Use `write-project-file` only when the user explicitly wants the file inside a project; those files are excluded from AI search.

## Choosing where a file goes

Before proposing a path, call `vault-overview` (and `browse-vault` on the likely folder) and fit the file into the existing structure. Propose one full path, e.g. `Reports/2026/Q3-board-update.md`, and wait for a yes. Do not invent a new top-level folder when an existing one fits.

Never write, overwrite or share a file without the user's explicit go-ahead.
