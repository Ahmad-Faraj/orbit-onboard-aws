---
name: orbit-onboard
description: Generate a new-contributor orientation for a GitLab project from the Knowledge Graph (Orbit). Use when someone is new to a codebase and asks where to start, what the important parts are, how it is structured, or who to ask. Produces a module map with an architecture diagram, the core abstractions to learn first (by call-graph centrality), the composition of the code, and recent contributors. Triggers on "I'm new to this repo", "where do I start", "how is this project structured", "give me a tour".
version: 0.2.0
license: MIT
metadata:
  audience: developers
  keywords: orbit, knowledge-graph, onboarding, architecture, codebase-map, gitlab
  workflow: ai
---

# Orbit onboard

The hardest part of joining a codebase is not reading code -- it is knowing
which code to read. This skill answers that from the Orbit knowledge graph
instead of guesswork: point it at a project and it produces a newcomer's map.

It answers five questions:

1. **Where does the code live?** -- the files with the most definitions.
2. **How is it organized?** -- the modules, and how they depend on each other,
   as an architecture diagram.
3. **What kind of code is it?** -- the mix of functions, methods, structs, etc.
4. **What should I learn first?** -- the definitions with the most callers, i.e.
   the abstractions the rest of the project leans on.
5. **Who do I ask?** -- the people who have merged work here most recently.

## Prerequisites

Requires `glab` v1.94.0+ with Orbit access. Verify with
`glab orbit remote status`. The project must be indexed by Orbit.

## Quick path

Run the bundled tool: `./orbit-onboard <project-path>`. It runs every query
below and prints the orientation, including a Mermaid architecture diagram.

## Workflow

### Step 1 -- where the code lives

Aggregate `Definition` nodes for the project, grouped by `file_path`, ordered by
count. The top files are where the project's surface area concentrates. See
[references/queries.md](references/queries.md#1-where-the-code-lives).

### Step 2 -- modules and architecture

Aggregate the `CALLS` edge grouped by both the caller's and the callee's
`file_path`, then roll each file path up to a module (its first two path
segments). Cross-module pairs are the architecture: which subsystem depends on
which. Render them as a Mermaid `graph LR` so the structure is visible at a
glance. See [references/queries.md](references/queries.md#2-module-dependencies).

### Step 3 -- composition

Aggregate `Definition` grouped by `definition_type`. This tells a newcomer the
shape of the code (method-heavy OO, struct-heavy systems code, and so on). See
[references/queries.md](references/queries.md#3-composition).

### Step 4 -- learn these first

Traverse the `CALLS` edge and count callers per callee (group by `fqn`). The
definitions with the most incoming calls are the project's spine -- learning
them first pays off fastest. See
[references/queries.md](references/queries.md#4-core-abstractions).

### Step 5 -- who to ask

Traverse `User --AUTHORED--> MergeRequest` (merged), ordered by recency, and rank
by frequency. See [references/queries.md](references/queries.md#5-recent-authors).

## Output

Assemble a short orientation grounded only in what the queries returned: a couple
of sentences on what the project is, the architecture diagram, the abstractions
to learn first, and who to ask. If the project has no call graph or no MR history
indexed, say so for that section rather than inventing entries.
