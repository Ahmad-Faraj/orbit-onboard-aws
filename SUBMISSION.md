# Devpost submission - orbit-onboard

**Track:** Showcase
**Best-fit category:** Quality of Idea (also strong on Potential Impact)

---

## The one-liner

Point it at any indexed project and it prints a new-contributor tour: a module
map with an architecture diagram, the handful of definitions to learn first, and
who to ask -- all from the GitLab Knowledge Graph.

## Inspiration

The hardest part of joining a codebase is not reading code -- it's knowing which
code to read. A newcomer opens a repo with hundreds of files and no idea which
ones matter, what the core abstractions are, or who to ask. The usual answer is
to guess, or to keep interrupting a senior engineer. But that knowledge already
exists in the shape of the code and its history -- which is exactly what Orbit
indexes. orbit-onboard reads it back as a guided tour.

## What it does

Run `orbit-onboard <project-path>` and it prints an orientation:

- **Where the code lives** -- the files with the most definitions.
- **Modules & architecture** -- the project's subsystems and how they depend on
  each other, rendered as a Mermaid diagram you can read at a glance.
- **What kind of code it is** -- the mix of functions, methods, structs, etc.
- **Learn these first** -- definitions ranked by how many other definitions call
  them. The most-called functions are the project's spine.
- **Who to ask** -- the people who've merged work here most recently.

## The idea worth judging

Everyone can list files. orbit-onboard does the two things a senior engineer
actually does for a newcomer: it **draws the architecture** (rolling the call
graph up to a module dependency diagram) and it **ranks what to read first by
call-graph centrality.** Instead of "here are 800
files," it says "these ten functions are what the project is built around -- start
there." That's how an experienced engineer actually explains a codebase, and it's
only cheap to compute because Orbit already holds the resolved call graph. On a
real project it surfaces exactly the right spine -- the query compiler's
`compile`, the ontology loader, the core test harness -- without anyone tagging
them as important.

## How we built it

A single Python script over the Orbit query API. "Where the code lives" and "what
kind of code" are aggregations over `Definition` grouped by `file_path` and
`definition_type`. "Learn these first" is an aggregation over the `CALLS` edge:
group by the callee, count distinct callers, order descending. "Who to ask"
traverses `User -AUTHORED-> MergeRequest` by recency.

## Why it's easy to adopt

- **One command to install:** `git clone ... && ./install.sh`.
- **One command to run:** just the project path.
- **Works as an Agent Skill** for the GitLab Duo Agent Platform and other agents.
- Sections with no data are reported honestly, not faked.

## Challenges

The key decision was choosing centrality -- incoming `CALLS` count -- as the
"importance" signal, rather than file size or churn. It's the one that best
matches how people actually orient newcomers: most of this doesn't matter yet;
these few things are the core.

## What's next

- Scope the tour to a directory or label for subsystem-level orientation.
- Add "recent merged MRs to read" as worked examples of how change happens here.
- Link each core definition to its file and line so an agent can open it.

## Links

- Repo (MIT): https://gitlab.com/Ahmad-Faraj/orbit-onboard
- Demo video: <add YouTube/Vimeo link>
- AI Catalog: <add link after publishing>
