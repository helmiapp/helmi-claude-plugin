---
name: projects
description: Answers questions about the current state of a project recorded in Helmi and writes updates back to it. Use when the user names a project (for example "the river documentary" or "the Series A"), or asks where things stand, what is happening, what changed, what is coming up, what is blocked, what was decided, when a shoot or deadline falls, what an email thread means for the work, or who a person or company is. Also use when the user says to log, note or record something on a project, or when a conversation settles a decision or finishes something the record does not yet know. Covers which Helmi tool answers which question, how much to retrieve before answering, and what the record does not contain.
---

# Helmi projects

All tool names below are on the Helmi MCP server bundled with this plugin.

## What a project is, and your job with it

A project in Helmi is one ongoing initiative with a record attached to it: a documentary in
production, a fundraise, a touring release. The record holds who is involved, which documents,
notes and meetings belong to it, the current facts extracted from those sources, its dated
milestones, its open questions, and what changed recently.

People do not maintain this record by hand. Sources get classified into it, facts get extracted
from those sources, and someone curates the rest occasionally. That is why the record is usually
right about what it has and silent about what it does not have.

Your job has two halves. Read the record before answering anything about the project, so the user
is not the one holding the state in their head. Write back to it when the conversation produces
something the record does not know, so the next person does not have to ask them.

## Answer only from the record

If the tools returned nothing on a point, say "not in my context" and stop. Do not fill the gap
from an adjacent email, a file attached to the chat, or a plausible pattern.

This is the failure that matters most here. Inferring a fact from a nearby source and stating it as
recorded is worse than an incomplete answer, because the user cannot tell the two apart. When you
state a fact, name where it came from: the email, document, meeting or note.

If you catch yourself reasoning "this probably means", stop and report what the record actually
says instead.

## When a message is a project question

Reach for the project record when the user:

- names a project, or names a shoot, deliverable or client that belongs to one
- asks where things stand, what is happening, what changed, what is next, what is late, what is
  blocked, or what someone is waiting on
- asks about a date: a shoot, a delivery, a screening, a deadline
- asks what was decided about something, or what was asked of whom
- asks what an email or thread means for the work
- pastes or attaches something and asks what it changes

You do not need the user to say the word "project". "Are we still shooting the 15th" is a project
question.

Do not reach for it when the question does not depend on project state: general knowledge, drafting
from a format the user already has, rewriting text they gave you, or a question about how to do
something. A project lookup that returns nothing useful still costs the user a wait.

## Which tool answers which question

| The user is asking about | Call | When |
|---|---|---|
| a project's state: what changed, what is open, what is next | `get-project` with the project name | first, before anything else |
| which project something belongs to | `list-projects` | only when the project was not named, or the name did not resolve |
| an email or a thread | `emails-list` to find the message, then `email-thread-context` with its id | always both, in that order; never summarize a thread from one message |
| who a person or company is | `search-entities` | a name appears that you cannot place |
| what a specific document says | `search-documents`, then `documents-get` | the user asked about that document, not about the project |
| what is pending, overdue or assigned | `list-tasks` with `projectSlug` | the user asked about tasks or workload, not project status |
| what was said in a meeting | `meetings-list`, then `meetings-get` | the user asked about that meeting |

`get-project` accepts a name, so when the user names the project you call it directly. Calling
`list-projects` first is a wasted round trip.

## How much to pull, and when to stop

`get-project` is already the whole-project read. It returns people, sources, facts, milestones,
asks and recent changes in one call. Treat its result as the answer, not as a table of contents to
go fetch.

1. **One retrieval call, then answer.** Make a second call only when the first returned something
   that names what is missing, such as a document id you now need the text of.
2. **Do not open the sources `get-project` listed.** They are there so you can cite them. Read one
   only when the user asks what that specific document or meeting says.
3. **Never run two search tools at the same question.** Match the tool to the noun: a project goes
   to `get-project`, a person to `search-entities`, an email to `emails-list`, document text to
   `search-documents`. Firing all of them is not thoroughness. The one route that is two calls by
   necessity is a thread: the finder, then `email-thread-context`.
4. **Do not call `get-project` twice in a conversation** unless the user says something changed or
   asks for a fresh check. The first result is still current.
5. **When the right call comes back empty, that is the answer.** Say the record has nothing on it.
   Do not widen into a search of everything to prove the absence. A trawl produces a longer reply,
   not a truer one.

## What the record may be missing

Say which of these applies when it matters, rather than presenting a partial record as complete.

- **Asks are entered by hand.** No extractor writes them. An empty list of asks means nobody
  entered one, not that nothing is blocked.
- **Milestones are curated by people too.** A milestone can be out of date. If one looks stale
  against something else you read, say so instead of picking a side.
- **Anything auto-classified can be wrong.** A person or source marked `origin: auto` was proposed
  by a classifier; `status: suggested` means nobody has confirmed it. Treat both as provisional.
- **The sources list is capped at 50 per type.** When `sourcesTotal` is higher than what came back,
  older sources exist and are not in your response. Do not conclude they are absent.
- **A file nobody classified into the project is not in the record**, even when it exists in
  someone's Drive or was attached to a different chat.
- **Nothing said in a Claude conversation reaches the record on its own.** If it was not logged, it
  is not there. That is what the next section is for.
- **Files attached to a Claude project are templates, formats and past examples.** They are not
  current state. Current state is in Helmi.

## Writing back to the record

**A note, `add-project-note`.** Takes `project`, `text`, and an optional `occurredAt`. Use it for
anything the record has no source for: a decision reached in this conversation, a verbal update, a
correction, a task someone says is finished. One short paragraph dated today, in the user's own
words, not a transcript and not your commentary.

You may write a note without being asked when the conversation clearly settled something. It is
append-only and attributed, so a wrong one is easy to correct. Say in one line what you logged, so
the user can correct it.

**A milestone, `manage-milestone`.** Use `action: update` with the `milestoneId` from
`get-project` when a date moves or a shoot is confirmed or cancelled. `action: create` for a dated
item the record does not have. Milestone `type` is shoot, deliverable or event; `state` is planned,
shot, tbc or cancelled. Use `datePrecision: month` when the exact day is not known yet.

**An ask, `manage-ask`.** Use `action: answer` with the `askId` from `get-project` when an open
question gets resolved in the conversation.

Milestones and asks are structured state that other people read on the project page, so confirm
with the user before changing one. Notes are append-only, so they do not need that.

## Answering "where are we on X"

Call `get-project`, then answer in this order, skipping anything the record has nothing for: what
changed since they last looked, open asks and blockers, the next dated milestones, then whatever
else they specifically asked. Do not list the people or the sources unless asked. They know who is
on their own project.

Illustrative shape:

```
Since you last looked, two things moved on Riverline.

- The factory shoot is confirmed for 15 to 17 March.
  (email from the producer, 2026-02-28)
- The teaser script is still open, with nobody assigned.
  (ask "teaser script", opened 2026-02-20)

Next dated: factory shoot 15 March, coastal block from 6 April.

On the budget sign-off: not in my context, the record has nothing about it.
```

Every claim carries its source, the open item is named as open, and the part the record cannot
answer is said plainly instead of filled in.

## Answering "what does this thread mean"

Find the message with `emails-list`, then call `email-thread-context` with its id. Use
`forwarded-emails-search` instead of `emails-list` when the thread was forwarded into Helmi rather
than living in the connected inbox.

`email-thread-context` takes an id (`emailId`, or `sourceIds` from a forwarded search) and has no
free-text argument, so you cannot start there: the finder call is a required first step, not an
optional one. Both calls, every time. Stopping at the finder and reading one message with
`emails-get` is the failure this section exists to prevent, because the reply that changes
everything is usually further down the thread.

Answer in three parts: what the thread is about in two sentences, what the latest message asks of
the user, then anything with a date on it. Report a name you could not resolve as unresolved rather
than guessing. If the thread belongs to a project, say which, and whether it changes anything
already on the record.

## Never

- Fill a gap in the record with a plausible guess.
- Summarize a thread from one message, or from `emails-get` without calling `email-thread-context`.
- Trawl multiple tools to avoid saying "not in my context".
- Change a milestone, ask or task without the user's go-ahead.
- Send an email or a message on the user's behalf. Draft it and let them send it.
