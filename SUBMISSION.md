# Devpost submission - orbit-onboard

**Track:** Showcase
**Best-fit category:** Quality of Idea (also strong on Potential Impact and Design & Usability)

---

## The one-liner

Drop into any project and, in seconds, get the map a senior engineer would draw
you: how the codebase is organized, what to read first, and who to ask -- all
from the GitLab Knowledge Graph.

## Inspiration

Every developer's first week on a new codebase is spent rebuilding a map that
already exists. You open a repo with hundreds of files and no idea which ones
matter, how the pieces fit, or who to ask -- so you guess, or you keep
interrupting whoever's been there longest. But that map isn't missing. It's
encoded in the call graph: what depends on what, what everything leans on, who
changed what. Orbit indexes exactly that. orbit-onboard just reads it back out.

To prove the point, the demo runs it on **GitLab's own Orbit codebase** -- the
very project this hackathon is built around -- and watches it draw a clean
architecture map of a 13,000-definition Rust workspace it has never seen before.

## What it does

Point it at a project (`orbit-onboard <path>`, or ask the agent "give me a
tour") and it produces a short, structured orientation:

- **A one-line summary** -- size, module count, and the shape of the code.
- **Architecture** -- the subsystems and how they depend on each other, rendered
  as a **Mermaid diagram** that displays as a real graph in GitLab, an MR, or
  Duo chat.
- **Learn these first** -- the definitions everything else calls the most: the
  project's spine, ranked.
- **Where the code lives** -- the biggest modules and densest files.
- **Who to ask** -- the people who've merged work here most recently.

## The idea worth judging

Everyone can list files. orbit-onboard does the two things a good senior engineer
actually does for a newcomer, and it does them from graph evidence, not guesses:

1. **It draws the architecture.** It rolls the resolved call graph up to the
   module level and renders the dependency structure as a diagram -- the mental
   model that normally takes a week to build in your head.
2. **It tells you what to read first by call-graph centrality.** Not the biggest
   files -- the definitions the rest of the code leans on most. On the Orbit
   codebase it surfaces exactly the right spine (the query compiler's `compile`,
   the ontology loader, the core test harness) without anyone tagging them.

Both are one query each, and only cheap because Orbit already holds the resolved
graph. Grep can't answer either: it can't draw a dependency diagram and it can't
rank by who-calls-what across the whole repo.

## Impact

Onboarding is one of the most universal, most expensive problems in software --
every team, every new hire, every internal transfer pays the "first week lost to
ramp-up" tax. orbit-onboard turns that week into seconds, and it scales to any
indexed repo for free -- no per-project setup, no maintenance, because the graph
is already there. It is equally useful to a human reading the output and to an AI
agent that needs to orient itself in an unfamiliar repo before doing real work.

## How we built it

A single, readable Python script (and an equivalent GitLab Duo agent) over the
Orbit query API. The architecture view is one aggregation over the `CALLS` edge
grouped by the caller's and callee's file, rolled up to modules and rendered as
Mermaid. "Learn these first" is a `CALLS` aggregation grouped by callee, counting
callers. The summary and module map come from a single `Definition`-by-file
query. Every section is grounded only in what the queries returned -- empty
sections are reported, never invented. Covered by a unit-test suite that runs in
CI.

## Why it's easy to adopt

- **One command to install** (`git clone ... && ./install.sh`) and **one to run**
  (just the project path).
- **Also a published GitLab Duo agent** -- ask it for a tour in chat and it
  renders the architecture diagram inline.
- **No backend, no per-project setup** -- it rides on the Orbit query API.

## What's next

- Scope the tour to a directory or label for subsystem-level orientation.
- Map each core definition to its file and line so an agent can open it directly.
- "Recent changes to read" -- the last few merged MRs as worked examples.

## Links

- Repo (MIT): https://gitlab.com/Ahmad-Faraj/orbit-onboard
- AI Catalog agent: <add link>
- Demo video: <add YouTube/Vimeo link>
