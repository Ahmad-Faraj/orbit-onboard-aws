[← README](../README.md) | **Requirements** | [Next: Architecture →](./02-architecture.md)

# 1. Requirements

## Functional

- Authenticated users submit a GitLab project path and receive a rendered orientation report.
- Generation is async - the API returns a `jobId` immediately; the client polls for `READY`.
- Results are cached by project path; a cache hit returns instantly with no worker invocation.
- The service holds one GitLab service-account token - users never supply their own.
- Finished reports are stored durably and served through CloudFront.
- Jobs that fail after retries are captured in a Dead-Letter Queue, not silently dropped.

## Non-Functional

- **Latency:** submit endpoint responds under 500 ms regardless of cache/queue path.
- **Availability:** no single component failure should take down the full service (managed multi-AZ services throughout).
- **Security:** WAF at edge, least-privilege IAM per function, secrets in Secrets Manager, KMS encryption at rest.
- **Cost:** fits AWS Free Tier at demo volumes; zero idle cost - every component scales to zero.
- **Observability:** distributed tracing (X-Ray) across the full job lifecycle; alarms on DLQ depth and Lambda error rate.

## Scale Anchor

Target: ~500-developer engineering org, developers occasionally onboarding to a new internal project.

| Signal | Number |
|---|---|
| Concurrent users (peak) | ~50 |
| Jobs per day | ~200 (most are cache hits) |
| Job duration (first run) | 10–60 s |
| Report size | 50–200 KB |

Comfortably within Lambda and SQS limits. SQS absorbs bursts; a single worker instance handles one job at a time.

## Out of Scope

- Multi-region active-active.
- Real-time streaming of partial output.
- Non-GitLab sources (the worker bundles `glab` and the Orbit API).
- Per-user GitLab tokens.

[← README](../README.md) | **Requirements** | [Next: Architecture →](./02-architecture.md)
