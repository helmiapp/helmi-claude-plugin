---
name: email
description: Reads and explains the user's email through Helmi. Use when the user asks to check their email, what is new in the inbox, what an email or thread means, what someone wants from them, or to find a message from a person or about a topic, including threads forwarded into Helmi.
---

# Email in Helmi

Email is read-only. Never claim to send or reply; draft the text and let the user send it.

## Routing

- **Check inbox / what's new:** `emails-list` with a date range (default the last 2 days) and unread filter if asked. Group the answer by what needs action from the user, then FYI. One line per message: sender, subject, the ask.
- **Explain a thread:** find the message with `emails-list` (or `forwarded-emails-search` for a forwarded thread), then ALWAYS call `email-thread-context` with that id. It takes an id, never free text, so it is always the second call. Never explain a thread from `emails-get` on one message: the reply that changes things is usually further down.
- **Who is this sender:** `search-entities` before guessing.
- **Does it touch a project:** if the thread belongs to a project, say which, and whether it changes anything on the record (`get-project`).

## Answer shape for a thread

1. What the thread is about, two sentences.
2. What the latest message asks of the user.
3. Anything with a date on it.
Report unresolved names as unresolved.

If `emails-list` errors with an access message, the user's account has no connected inbox; say so and stop.
