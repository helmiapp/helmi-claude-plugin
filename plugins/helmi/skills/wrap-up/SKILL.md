---
name: wrap-up
description: Reviews the current session and proposes what to save to Helmi (decisions as project notes, documents as vault files, follow-ups as tasks), writing only what the user approves. Use when the user says wrap up, save this to Helmi, log what we did, or when a Helmi plugin hook asks you to offer it.
---

# Wrap up a session into Helmi

1. **Collect candidates** from this session only:
   - decisions that were settled, and updates the record does not have: project notes
   - files you wrote that someone else will read (reports, plans, briefs, exports): vault files
   - commitments with an owner ("I'll send X by Friday"): tasks
   Skip scratch work, code, and anything Helmi already holds. Zero candidates is a valid result: say "nothing worth saving" and stop.
2. **Resolve targets** with at most one call per kind: `list-projects` for the project slug, `vault-overview` (then `browse-vault`) for a folder that fits, `list-tasks` to avoid duplicating an existing task.
3. **Propose one numbered list**, one line each, with the exact target:
   ```
   1. Note on riverline: "Shoot moved to 15-17 Mar, confirmed by the producer." (add-project-note)
   2. File Reports/2026/q3-board-update.md from ./q3-board-update.md (upload-vault-file)
   3. Task in riverline: "Send revised budget to the client", due 2026-03-09 (manage-task)
   ```
   Ask: "Which should I save? (all / numbers / none)".
4. **Write only the approved items**, then report one line per item with what was written and where. On an error, report it; do not retry silently.

Tool details: notes use `add-project-note` (`project`, `text`, optional `occurredAt`), or `create-note` when there is no project. Files follow the `documents` skill (text via `content`, binary via request-upload then commit-upload). Tasks follow the `tasks` skill.

Never write anything before the user answers step 3.
