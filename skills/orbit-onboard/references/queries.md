# Query reference

Every query goes through `glab orbit remote query <file>`. Replace `$PID` with
the numeric project id (`glab api projects/<url-encoded-path> | jq .id`).

## 1. Where the code lives

```json
{
  "query": {
    "query_type": "aggregation",
    "nodes": [
      {"id": "d", "entity": "Definition",
       "filters": {"project_id": {"op": "eq", "value": $PID}}}
    ],
    "group_by": [{"kind": "property", "node": "d", "property": "file_path", "alias": "file"}],
    "aggregations": [{"function": "count", "target": "d", "alias": "n"}],
    "aggregation_sort": {"column": "n", "direction": "DESC"},
    "limit": 10
  }
}
```

## 2. Module dependencies

Aggregate the `CALLS` edge grouped by both the caller's and the callee's
`file_path`. Roll each path up to a module (first two segments) client-side and
keep the pairs where the modules differ -- those are the cross-module
dependencies. Render them as a Mermaid `graph LR`.

```json
{
  "query": {
    "query_type": "aggregation",
    "nodes": [
      {"id": "caller", "entity": "Definition", "filters": {"project_id": {"op": "eq", "value": $PID}}},
      {"id": "callee", "entity": "Definition", "filters": {"project_id": {"op": "eq", "value": $PID}}}
    ],
    "relationships": [{"type": "CALLS", "from": "caller", "to": "callee"}],
    "group_by": [
      {"kind": "property", "node": "caller", "property": "file_path", "alias": "from"},
      {"kind": "property", "node": "callee", "property": "file_path", "alias": "to"}
    ],
    "aggregations": [{"function": "count", "target": "caller", "alias": "n"}],
    "aggregation_sort": {"column": "n", "direction": "DESC"},
    "limit": 1000
  }
}
```

## 3. Composition

Same as query 1, grouped by `definition_type` instead of `file_path`.

## 4. Core abstractions

Count incoming `CALLS` edges per definition. High counts mean the rest of the
code depends on it.

```json
{
  "query": {
    "query_type": "aggregation",
    "nodes": [
      {"id": "caller", "entity": "Definition"},
      {"id": "callee", "entity": "Definition",
       "filters": {"project_id": {"op": "eq", "value": $PID}}}
    ],
    "relationships": [{"type": "CALLS", "from": "caller", "to": "callee"}],
    "group_by": [{"kind": "property", "node": "callee", "property": "fqn", "alias": "fn"}],
    "aggregations": [{"function": "count", "target": "caller", "alias": "callers"}],
    "aggregation_sort": {"column": "callers", "direction": "DESC"},
    "limit": 10
  }
}
```

## 5. Recent authors

```json
{
  "query": {
    "query_type": "traversal",
    "nodes": [
      {"id": "u", "entity": "User", "columns": ["username"]},
      {"id": "mr", "entity": "MergeRequest", "columns": ["iid"],
       "filters": {"project_id": {"op": "eq", "value": $PID}, "state": "merged"}}
    ],
    "relationships": [{"type": "AUTHORED", "from": "u", "to": "mr"}],
    "order_by": {"node": "mr", "property": "merged_at", "direction": "DESC"},
    "limit": 30
  }
}
```

Count how often each username appears to rank candidates.

## Notes

- `filters` is an object keyed by property name, not an array.
- Aggregation queries need a filter on at least one node.
- `group_by` accepts up to 4 keys; query 2 uses two (caller and callee file).
- `Definition` properties used here: `file_path`, `definition_type`, `fqn`,
  `project_id`.
