---
name: save
description: Saves one local file into the Helmi vault at a location that fits the existing folder structure, after the user confirms the path. Use when the user says save this file to Helmi, upload this to the vault, or when a Helmi plugin hook suggests a document may belong in Helmi.
argument-hint: <path>
---

# Save a file to Helmi

1. Take the file from the argument, or the document just written in this session. Read it enough to know what it is.
2. Decide whether it belongs in Helmi at all: something other people will read or need later (report, brief, plan, deck, export). Scratch notes, code and config do not. If it does not belong, say so in one line and stop.
3. Call `vault-overview`, then `browse-vault` on the most likely folder. Propose ONE full vault path that fits the existing structure, plus a project if it clearly belongs to one. Wait for a yes or a different path.
4. Upload with `upload-vault-file`:
   - text up to 5 MB: `action: create`, `path`, `content`, `createParents: true`
   - binary or larger: `request-upload` with `sizeBytes`, run the returned curl on the local file, then `commit-upload` with the `uploadId`
   If the path is taken, ask before using `action: update` (it keeps the old version).
5. Reply with the saved path in one line.
