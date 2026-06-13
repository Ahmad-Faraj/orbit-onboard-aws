# Devpost submission - orbit-onboard

**Track:** Showcase
**Best-fit category:** Quality of Idea (also strong on Design & Usability)

---

## Inspiration

Every developer remembers the first week on a new codebase: hundreds of files,
no idea which ones matter, and the only way forward is to guess or to keep
interrupting a senior engineer. The strange part is that the answer already
exists -- in the structure of the code and its history. The most important files
are the ones with the most code; the most important functions are the ones
everything else calls; the people to ask are the ones who just merged work here.
Orbit indexes all of that. orbit-onboard reads it back as a guided tour.

## What it does

Point it at a project and it prints a new-contributor orientation:

- **Where the code lives** -- the files with the most definitions.
- **What kind of code it is** -- the mix of functions, methods, structs, etc.
- **Learn these first** -- the definitions ranked by how many other definitions
  call them. The most-called functions are the project's spine, so they're the
  ones worth understanding first.
- **Who to ask** -- the people who've merged work here most recently.

## How we built it

A single Python script over `glab orbit remote query`. "Where the code lives"
and "what kind of code" are aggregations over `Definition` grouped by
`file_path` and `definition_type`. The interesting one, "learn these first," is
an aggregation over the `CALLS` edge: group by the callee and count distinct
callers, highest first. That call-graph centrality is the novel signal -- it
turns "which functions matter" from an opinion into a query. "Who to ask"
traverses `User -AUTHORED-> MergeRequest` by recency.

## Why this is more than a file listing

A file tree tells you what exists; it doesn't tell you what's important.
Ranking by call-graph centrality is the difference between "here are 800 files"
and "these ten functions are what the project is built around -- start there."
That ranking is only practical because Orbit already holds the resolved call
graph; computing it from scratch would mean parsing and resolving the whole
codebase.

## Challenges

The key design decision was choosing centrality (incoming `CALLS` count) as the
"importance" signal rather than file size or churn. It's the one that best
matches how an experienced engineer actually explains a codebase: "don't worry
about most of this -- these few things are the core."

## What's next

- Scope the orientation to a directory or label for subsystem-level tours.
- Add "recent merged MRs to read" as worked examples of how change happens.
- Link each core definition to its file and line so an agent can open it.

## Links

- Repo (MIT): https://gitlab.com/Ahmad-Faraj/orbit-onboard
- Demo video: <add YouTube/Vimeo link>
- AI Catalog: <add link after publishing>
