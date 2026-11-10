---
name: media-library
description: Find, check and pitch material from Helmi Productions' archive of footage, photos and interview transcripts with the `media_*` tools. Use when someone asks what Helmi has on a topic, place, person or project, wants a quote or b-roll, wants reel or documentary ideas from existing material, or asks who appears in or what is said in the footage.
---

# Helmi media library

The `media_*` tools search Helmi Productions' archive: ~7k videos (interviews, b-roll, events), ~14k photos, interview
transcripts and their translation docs. Everything is read-only.

## How to work

1. **Start broad, then narrow.** `media_overview` (optionally with `query` and filters) shows what a slice holds:
   where it was filmed, what it talks about, who is on camera, themes, shoots, top interviews and quotes. Every value it
   returns can be passed back as a filter, so narrow by reusing them rather than guessing spellings.
2. **Filmed in vs talked about are different.** `country` / `place` filters are where footage was shot; `about` is what
   people talk about (a US interview about Singapore has `about: Singapore`). For a place, check both.
3. **Themes.** `media_subjects` gives the table of contents of any slice (broad themes → sub-themes, by number of
   files). Use a theme id as the `theme` filter.
4. **Find the material.** `media_search` with `level`: `quotes` (what was said), `videos` / `photos` (what is seen),
   `files`, `docs`. Use the `about`, `person`, `content` (interview, b-roll…), `shot_size`, `usable` filters.
   **When nothing may be missed** ("pull every clip of X", a shot list from a client), don't rely on queries: a query
   ranks the best matches and stops near 100. Set the scope with filters (`country`, `shoot`, `project`, `origin`,
   `vantage`…), leave `query` empty, `limit=50`, and page with `offset` until no more exist; read every description
   and sort them into the list yourself. Then run a few queries without the scope filter to catch material filed
   elsewhere (interviews that describe it, edits, other folders).
5. **Check before you commit.** Read the words with `media_get_transcript` (a range around the quote) and look at the
   picture with `media_view_frames` (one contact sheet). Don't pitch a clip you haven't checked. Ask for ranges, not
   whole transcripts: a whole interview is up to ~8k tokens, a few minutes around a quote is ~1k. The default `packed`
   format is one line per stretch of one speaker; `format="full"` only when you need the stored turns.
6. **Read the folder.** Every result shows the file's folder, e.g. `Interviews/Interviews_GenZero/C0242.MP4`. The folder
   usually names the interviewee's organisation or the shoot: use it to say who is speaking when the speaker label is
   just `SA`.
7. **Preview or original.** `media_view_frames` and `media_get_media` take `quality`. `preview` (default) is 720p and
   fast (1-3 s): use it to look, check and share candidates. `original` is the camera file at full resolution and slow
   (frames about 5-20 s, clips a minute or more, longer for long ranges): use it only for what goes into a cut (crops,
   final frames, checking focus or text), with the shortest range you need.
8. **Links.** Every result carries a link to the team's review UI, `<https://media-library.helmi.com/f/ID?t=323.5>`, that
   opens the file at that moment (a quote starts just before, with the words highlighted). **Always include the link
   next to every file you cite, so the user can open it.** Copy it as given; to link another moment of a file, change
   `t` (and `end`) to seconds, as the transcript header shows. These links don't expire. `media_get_media(file_id,
   start_s, end_s)` is different: a short-lived link to play or download a clip (or the photo) file itself.
9. **Batch, don't loop.** To read, look at or link several files, pass them together in `items` (up to 12) in one
   call of `media_get_file`, `media_get_transcript`, `media_view_frames` or `media_get_media`: one call per file costs
   a turn each.
10. **Cite everything.** Every quote or shot you propose names its file (with its folder), timecode and link, from a
   tool result.

## Pitching a reel

For each idea: a working title, the angle in one or two sentences, 3–6 quotes (speaker if known, file, timecode, the
words, the link), the b-roll to cover them (file + timecode + link, why it fits), and the gaps (what we don't have). Mark anything you
are unsure of.

## Known limits

- Speakers in transcripts are often labelled `SA`, `SB`…; where the index knows the name it shows `Name (SA)`. The
  overview and file summaries sometimes name them too. Say so when a name is a guess.
- Only faces someone named are searchable by person. A face on screen is not the speaker: in interviews the
  interviewer is often in shot too.
- The same answer often exists in several takes or copies; pick one and mention the others.
- Some quotes are in Spanish, Portuguese or other languages; translations exist for some interviews.

## Feedback

When a tool was missing, confusing, too slow or returned too much, call `media_feedback` with a short note (and the
tool's name). It goes to the people improving the tools.
