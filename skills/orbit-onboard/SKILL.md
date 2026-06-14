---
name: orbit-onboard
description: Generate a new-contributor orientation for a GitLab project from the Knowledge Graph (Orbit). Use when someone is new to a codebase and asks where to start, what the important parts are, how it is structured, or who to ask. Produces a one-line summary, a module map with an architecture diagram, the core abstractions to learn first (by call-graph centrality), where the code lives, and recent contributors. Triggers on "I'm new to this repo", "where do I start", "how is this project structured", "give me a tour".
version: 0.3.0
license: MIT
metadata:
  audience: developers
  keywords: orbit, knowledge-graph, onboarding, architecture, codebase-map, gitlab
  workflow: ai
---

# Orbit onboard

The hardest part of joining a codebase is not reading code -- it is knowing
which code to read. This skill answers that from the Orbit knowledge graph
instead of guesswork: point it at a project and it produces a newcomer's map --
a one-line summary, then the four things that actually orient someone.

1. **How is it organized?** -- the modules, and how they depend on each other,
   as an architecture diagram.
2. **What should I learn first?** -- the definitions with the most callers, i.e.
   the abstractions the rest of the project leans on.
3. **Where does the code live?** -- the modules and files with the most definitions.
4. **Who do I ask?** -- the people who have merged work here most recently.

## Prerequisites

Requires `glab` v1.94.0+ with Orbit access. Verify with
`glab orbit remote status`. The project must be indexed by Orbit.

## Quick path

Run the bundled tool: `./orbit-onboard <project-path>`. It runs every query
below and prints the orientation, including a Mermaid architecture diagram.

## Workflow

Open with a one-line summary -- total definition count, module count, and the
dominant definition types -- from a quick `Definition` count grouped by
`definition_type`. Then:

### Step 1 -- architecture

Aggregate the `CALLS` edge grouped by both the caller's and the callee's
`file_path`, then roll each file path up to a module (its first two path
segments). Cross-module pairs are the architecture: which subsystem depends on
which. Render them as a Mermaid `graph LR` so the structure is visible at a
glance. See [references/queries.md](references/queries.md#2-module-dependencies).

### Step 2 -- learn these first

Traverse the `CALLS` edge and count callers per callee (group by `fqn`). The
definitions with the most incoming calls are the project's spine -- learning
them first pays off fastest. See
[references/queries.md](references/queries.md#4-core-abstractions).

### Step 3 -- where the code lives

Aggregate `Definition` nodes grouped by `file_path` (rolled up to modules for the
overview, kept at file level for the detail). The biggest modules and files are
where the project's surface area concentrates. See
[references/queries.md](references/queries.md#1-where-the-code-lives).

### Step 4 -- who to ask

Traverse `User --AUTHORED--> MergeRequest` (merged), ordered by recency, and rank
by frequency. See [references/queries.md](references/queries.md#5-recent-authors).

## Output

Assemble a short orientation grounded only in what the queries returned: the
one-line summary, the architecture diagram, the abstractions to learn first,
where the code lives, and who to ask. If the project has no call graph or no MR
history indexed, say so for that section rather than inventing entries.
