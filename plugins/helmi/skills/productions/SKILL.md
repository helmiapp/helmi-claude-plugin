---
name: productions
description: Works a documentary production in Helmi stage by stage. Use when the user works on a project whose get-project shows kind production, asks what to do next on a film, where a production stands, what is missing for its stage, or asks to move its stage, record a funder, crew member, shoot, deliverable or release, or follow up a thread. Covers the stage checklist, what Claude does in each stage, and which tool writes each result back.
---

# Helmi productions

Everything in the `projects` skill applies: answer only from the record, cite sources, never fill
a gap with a guess. This skill adds the production stage and what to do in it. Tool names are on
the Helmi MCP server.

## Start from get-project

Call `get-project` by name before anything else. Read, in this order:

1. **Stage** and its date: Spark, Researching, Pitched, Funded, In production, Released, Killed.
2. **Open stage proposal.** Jev proposes a stage from the latest sources; it never moves the stage
   itself. A person confirms it. Show the proposal with its source and confidence. Confirm it with
   `update-project` (`stage`) only when the user agrees in this conversation. Never confirm on your
   own, and never set a stage from your own reading of the record. If the user says the proposal is
   wrong, dismiss it with `update-project` (`dismiss_stage_proposal: true`); the stage stays as it is.
3. **Checklist** for the stage: each item is filled (value and source) or missing. Missing means
   no visible evidence. Calls and WhatsApp never reach Helmi, so ask the user instead of assuming
   it has not happened.
4. **Threads that owe a move.** Say who owes the next move: us or them.
5. **Milestones relative to today.** A past `planned` milestone with no later evidence is
   unconfirmed; ask before treating it as done or missed.

Open with the stage, then what is missing, then what is due or owed. Skip what the record has
nothing for.

## What to do per stage

| Stage | Work with the user |
|---|---|
| Spark | Shape the concept (premise, angle), early research |
| Researching | Collect news, draft proposals, cold outreach to experts and partners |
| Pitched | Communications, cold outreach for funding, follow-ups |
| Funded | Contracts, scripts, shoot planning |
| In production | Shoot operations, clip selection, edit |
| Released | Distribution, marketing, impact analysis |
| Killed | Nothing. Record the reason if the user gives one |

Checklist per stage (what should be known or exist by then):

- **Spark:** `concept.premise`, `concept.angle`, who raised it, a research note.
- **Researching:** saved articles, a proposal document, `prospect` entities, `concept.format`.
- **Pitched:** `prospect` entities contacted, a pitch deck or one-pager, `funding.ask`, live
  threads with a next-move owner.
- **Funded:** a `funder`, `funding.committed`, a contract milestone, a script document, shoot
  milestones with locations and `crew`, deliverable milestones with due dates.
- **In production:** shoot milestones `done`, deliverables in progress with their files, marketing
  materials started.
- **Released:** a `distributor` or `broadcaster`, release and screening milestones,
  `release.date`, `release.platform`, `impact.*`.
- **Killed:** `killed.reason`, if a source says it.

Work the missing items first, then the stage's operations. Do not start the next stage's work
until the user says the stage has moved.

## Write back

Only through these tools. Say in one line what you wrote.

| Result | Tool |
|---|---|
| Stage change the user agreed to | `update-project` with `stage` |
| A proposal, script, brief or deck you drafted | `write-project-file` |
| A person or company with a role | `manage-participant` with `role` |
| A value that is now true, or one the user confirms | `manage-fact`, `add` or `confirm`, with `slot` |
| Shoots, deliverables, contract, funding, release, screening | `manage-milestone` |
| A thread dealt with elsewhere, or dropped | `manage-thread`, `handled` or `stopped` |
| A decision, or something said on a call | `add-project-note` |

Roles (fixed list): `funder`, `prospect`, `commissioner`, `partner`, `broadcaster`, `distributor`,
`subject`, `crew`, `location_contact`, `advisor`, `helmi`.

Slots (v1): `concept.premise`, `concept.angle`, `concept.format`, `funding.ask`,
`funding.committed`, `funding.source`, `fee`, `rights.territory`, `release.date`,
`release.platform`, `impact.views`, `impact.screenings`, `impact.press`, `killed.reason`. Use a
slot only for a value in this list; anything else is a note.

Milestone types: `pitch`, `meeting`, `contract`, `funding`, `shoot`, `deliverable`, `release`,
`screening`, `event`. States: `planned`, `tbc`, `done`, `delivered`, `missed`, `cancelled`. Use
`datePrecision: month` when the day is not known.

Notes are append-only and need no confirmation. Stage, facts, milestones, participants and threads
are shared structured state: confirm with the user before changing one, except to record
something they just told you.

## Never

- Move the stage without the user's agreement.
- Read "missing" as "did not happen".
- Send an email or a message on the user's behalf. Draft it, save it with `write-project-file` if
  asked, and let the user send it.
- Use a role or slot outside the lists above.
