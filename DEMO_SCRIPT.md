# Demo video script (~2 min)

Under 3 minutes, public on YouTube/Vimeo, no copyrighted music. Record your
terminal. Point the tool at a real, well-indexed project for the best output.

## 0:00-0:20 - the problem

> "Your first week on a new codebase: hundreds of files, no idea which ones
> matter or who to ask. The answer already exists in the structure of the code.
> orbit-onboard reads it out of the GitLab knowledge graph."

## 0:20-0:45 - run it

Run: orbit-onboard <project-path>

> "One command, one project path."

Let the orientation print.

## 0:45-1:15 - where the code lives + composition

Point at the first two sections.

> "First, where the code actually lives - the files with the most definitions.
> And the shape of it: method-heavy, struct-heavy, however this project is built."

## 1:15-1:50 - learn these first (the centerpiece)

Point at the most-called definitions.

> "This is the part that matters. These aren't the biggest files - they're the
> definitions the rest of the code calls the most. Orbit already has the call
> graph, so ranking the core abstractions is one query. Learn these ten things
> and you understand the spine of the project."

## 1:50-2:10 - who to ask + close

> "And the people who've merged here most recently - your who-to-ask list.
> That's orbit-onboard: a new-contributor tour, generated from the graph.
> Open source, MIT."

Show the repo URL: gitlab.com/Ahmad-Faraj/orbit-onboard
