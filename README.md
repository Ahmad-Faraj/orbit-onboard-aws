# orbit-onboard

An [agent skill](https://docs.gitlab.com/orbit/ai_coding_agents/) and CLI tool
that turns a project into a new-contributor orientation, using the GitLab
Knowledge Graph (Orbit).

## The problem

The hardest part of joining a codebase is not reading code -- it is knowing
which code to read. A new contributor opens a repo with hundreds of files and no
idea which ones matter, what the core abstractions are, or who to ask. The usual
answer is to guess, or to wait for a senior engineer to explain. That knowledge
already exists in the structure of the code and its history -- which is exactly
what Orbit indexes.

## What it does

Point it at a project and it prints an orientation built from four Orbit queries:

| Section | Question | How |
|---------|----------|-----|
| Where the code lives | Which files matter? | `Definition` count grouped by `file_path` |
| What kind of code | What's the shape? | `Definition` count grouped by `definition_type` |
| Learn these first | What's the spine? | Incoming `CALLS` edges per definition |
| Who to ask | Who works here? | `User -AUTHORED-> MergeRequest`, by recency |

The **"learn these first"** section is the interesting one. Instead of guessing,
it ranks definitions by how many other definitions call them. The functions with
the most callers are the ones the whole project leans on -- so they are the ones
worth understanding first. That ranking is only cheap to compute because Orbit
already holds the resolved call graph.

## Run it

```bash
./orbit-onboard gitlab-org/orbit/knowledge-graph
```

Real output (abbreviated) against an indexed project:

```
Orientation for ahmad-faraj-group/knowledge-graph
============================================================
A starting map of this project, built from the Orbit knowledge graph.

Where the code lives (top files by definitions)
-----------------------------------------------
    484  clients/gkgpb/gkg.pb.go
    246  crates/ontology/src/entities.rs
    205  crates/code-graph/src/v2/dsl/types.rs
    ...

Learn these first (most-called definitions)
-------------------------------------------
    175 callers  compiler::compile
    163 callers  containers::server::data_correctness::helpers::run_query
    ...
  These are the definitions the rest of the code leans on most.
```

Sections with no data in the graph are reported as empty, not faked.

## Install

```bash
git clone https://gitlab.com/Ahmad-Faraj/orbit-onboard.git
cd orbit-onboard && ./install.sh
```

Needs Python 3 and `glab` v1.94.0+ with Orbit access (`glab orbit remote
status`). The directory is also a valid agent skill -- drop it into an agent's
skills path and it activates on prompts like *"I'm new to this repo, where do I
start?"*. See [SKILL.md](SKILL.md), [references/queries.md](references/queries.md),
and [CATALOG.md](CATALOG.md) to publish it as an AI Catalog agent.

## Future direction

- Accept a directory or label to scope the orientation to one subsystem.
- Add "recent changes to read" -- the last few merged MRs with titles, as
  worked examples of how change happens here.
- Link each core definition to its file and line so the agent can open it.

## License

MIT -- see [LICENSE](LICENSE).
