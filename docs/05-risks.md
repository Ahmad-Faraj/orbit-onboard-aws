[← README](../README.md) | [← Well-Architected](./04-well-architected.md) | **Risks** | [Next: Future Work →](./06-future-work.md)

# 5. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **GitLab / Orbit API unavailable** | Medium | High | SQS retries up to `maxReceiveCount`. On exhaustion the message goes to the DLQ. CloudWatch alarm on DLQ depth alerts the operator. |
| **Worker Lambda timeout** on a very large repo | Low | Medium | Lambda's 15-minute limit covers current Orbit repos. If needed, the same Dockerfile deploys to ECS Fargate with no code changes. |
| **GitLab token leaked** via logs or an over-privileged role | Low | High | Token injected at runtime from Secrets Manager only. Never logged, never in the image. Only the worker IAM role has `GetSecretValue`. CloudTrail records every access. |
| **Cache staleness** - cached report reflects an old repo state | High | Low | Cache TTL expires entries within 7 days. Cache key can be extended with the latest commit SHA to invalidate on every merge. |
| **Worker crash causes duplicate job run** | Low | Low | The worker writes to S3 and DynamoDB only after full generation. A re-run overwrites the same key with the same result - idempotent. |
| **WAF false positive** blocks a valid project path | Low | Medium | Project paths are short alphanumeric strings. If a managed rule triggers, it can be scoped or overridden without removing WAF. |
| **Cost overrun** from a submission loop bug | Low | Low | AWS Budgets alert at $5. Cache short-circuits repeated identical submissions. DynamoDB on-demand and Lambda both have account-level concurrency limits. |

[← README](../README.md) | [← Well-Architected](./04-well-architected.md) | **Risks** | [Next: Future Work →](./06-future-work.md)
