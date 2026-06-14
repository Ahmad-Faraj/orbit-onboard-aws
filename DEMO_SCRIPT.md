# Demo video script (~2.5 min)

Under 3 minutes, public on YouTube/Vimeo, no copyrighted music. Point the tool
(or the agent) at a real, code-heavy project for the best output.

## 0:00-0:20 - the problem

> "Your first week on a new codebase: hundreds of files, no idea which ones
> matter, how it's structured, or who to ask. A senior engineer would draw you a
> map. orbit-onboard draws that map from the GitLab knowledge graph - in one
> command."

## 0:20-0:45 - run it

Run: orbit-onboard <project-path>   (or ask the Orbit Onboard agent in Duo:
"I'm new to this project, give me a tour.")

Let the orientation print.

## 0:45-1:30 - the architecture diagram (the hero)

Scroll to "How the modules connect" and the Mermaid diagram. If you're in Duo or
an MR, the diagram renders as an actual graph.

> "This is the part that takes a newcomer a week to build in their head: how the
> subsystems depend on each other. Orbit already has every call edge, so rolling
> it up to a module map is one query - and it renders as a real architecture
> diagram. You can see at a glance that the tests lean on the testkit and the
> query engine, that the indexer drives the ClickHouse client, and so on."

## 1:30-2:00 - learn these first

Point at the most-called definitions.

> "Then: what to read first. Not the biggest files - the definitions the rest of
> the code calls the most. These are the project's spine. Learn these ten things
> and the rest falls into place."

## 2:00-2:20 - who to ask + close

> "And the people who've merged here most recently - your who-to-ask list.
> That's orbit-onboard: the architecture, the core abstractions, and the people -
> the whole orientation, generated from the graph. Open source, MIT, and it runs
> as a GitLab Duo agent."

Show the repo URL: gitlab.com/Ahmad-Faraj/orbit-onboard
