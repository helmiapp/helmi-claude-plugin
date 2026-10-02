---
name: tasks
description: Reads and updates the user's tasks in Helmi. Use when the user asks what is on their plate, pending, due, overdue or blocked; when they mention finishing, shipping or starting something that might be tracked; or when they describe new work they intend to do.
---

# Tasks in Helmi

## Reading (free)

`list-tasks` answers most questions:
- "what do I owe today": `assignedToMe=true`, `dueWithin="today"`, `statuses=["open"]`
- "what's overdue": `dueWithin="overdue"`
- "what's blocked": `statuses=["open"]`, then rows with `isBlocked`
- one project: `projectSlug`

`get-my-day` adds this week's calendar, open asks and upcoming milestones; use it for "what's my day/week". `get-task` for one task's detail. `list-suggestions` shows AI-proposed task changes.

Present tasks grouped by project, overdue first, one line each: title, deadline, status.

## Writing (only after a clear yes)

`manage-task`:
- create: `action: create`, `projectSlug`, `title`, optional `deadlineDate` or `deadlinePhrase` with `referenceDate` set to today
- start or finish: `action: update` with `status: in-progress`, or `action: complete`
- note progress: `action: add-note`
- approve an AI suggestion: `review-suggestion`

## Guardrails

- Propose, then act. Never create, complete or change a task without a yes.
- Suggest once. If the user passes, drop it.
- Check `list-tasks` for an existing task before creating a duplicate.
- Ask for a deadline; never invent one.
- Only touch the user's own tasks unless they say otherwise. Match their language.
