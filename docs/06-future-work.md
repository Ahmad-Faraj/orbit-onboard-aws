[← README](../README.md) | [← Risks](./05-risks.md) | **Future Work** | [Next: Appendix →](./07-appendix.md)

# 6. Future Work

**Commit-keyed cache.** Include the latest commit SHA in the cache key so orientations refresh automatically when new code is merged, without waiting for the TTL.

**Webhook-triggered refresh.** A GitLab webhook on MR merge enqueues a background regeneration job via API Gateway. The next request gets a fresh report with zero wait.

**Step Functions orchestration.** Wrap the worker in a state machine to run Orbit query sections in parallel, enable per-step retries with exponential backoff, and support partial results if one query times out.

**EventBridge scheduled pre-warming.** A nightly schedule pre-generates orientations for the organisation's most active repos and warms the cache before the working day starts.

**CloudFront signed URLs.** Short-expiry signed URLs ensure only the requesting user can fetch their report.

**ECS Fargate worker.** If any repo pushes past Lambda's 15-minute limit, the same Dockerfile deploys to Fargate via EventBridge Pipes - no code changes required.

[← README](../README.md) | [← Risks](./05-risks.md) | **Future Work** | [Next: Appendix →](./07-appendix.md)
