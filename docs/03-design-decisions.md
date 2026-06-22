[← README](../README.md) | [← Architecture](./02-architecture.md) | **Design Decisions** | [Next: Well-Architected →](./04-well-architected.md)

# 3. Design Decisions

**3.1 Container-image Lambda vs zip Lambda for the worker.**
Options: zip Lambda, container-image Lambda, ECS Fargate, EC2.
Choice: **Container-image Lambda.**
Rationale: The worker shells out to the `glab` CLI binary. A zip Lambda cannot ship a standalone binary cleanly without layer gymnastics. A container image bakes `glab` + Python into one artifact in ECR. Lambda still gives scale-to-zero with no infrastructure to manage. Fargate works but adds VPC/NAT cost the workload doesn't justify. EC2 rejected - no idle servers.

**3.2 Asynchronous SQS vs synchronous API-to-worker.**
Options: API Gateway → Worker Lambda (sync), API Gateway → SQS → Worker (async).
Choice: **Async via SQS.**
Rationale: Orbit queries on a large repo can run 10–60 seconds. A synchronous call would hit API Gateway's 29-second integration timeout and has no retry on failure. Async returns a `jobId` in milliseconds, the worker runs in the background, and the DLQ handles failures.

**3.3 DynamoDB cache vs no cache vs ElastiCache.**
Options: recompute every request, DynamoDB with TTL, ElastiCache Redis.
Choice: **DynamoDB with TTL.**
Rationale: The same repo gets requested repeatedly across a team. Caching eliminates redundant worker runs and GitLab API calls. DynamoDB on-demand fits the read/write volume with zero idle cost. ElastiCache adds a VPC, NAT Gateway, and an always-on node - not justified here.

**3.4 One service-account token vs per-user tokens.**
Options: single token in Secrets Manager, per-user tokens in DynamoDB, OAuth per user.
Choice: **Single token in Secrets Manager.**
Rationale: Centralising the token removes the per-user `glab` setup requirement. Secrets Manager provides rotation and a full audit trail of every access via CloudTrail. The trade-off is all queries run under one identity, so the token scope must be read-only and minimal.

**3.5 Static SPA on S3 + CloudFront vs server-rendered frontend.**
Options: static SPA on S3 + CloudFront, server-rendered on Lambda or Fargate.
Choice: **Static SPA.**
Rationale: The frontend is a form, a status poller, and a report viewer - nothing requiring server-side rendering. S3 + CloudFront gives global low-latency delivery, zero idle cost, no cold starts, and a smaller attack surface. A server-rendered option adds a compute tier the workload doesn't need.

**3.6 Dead-Letter Queue vs discard on failure.**
Options: drop messages after max retries, route to a DLQ.
Choice: **DLQ.**
Rationale: Failed jobs must not be silently lost. The DLQ preserves them for inspection and manual replay. A CloudWatch alarm on DLQ depth makes failures visible immediately. Cost is negligible.

**3.7 Cognito vs custom JWT vs no auth.**
Options: Cognito User Pool, custom JWT in Lambda, no auth.
Choice: **Cognito User Pool.**
Rationale: Cognito gives sign-up, sign-in, MFA, password reset, and JWKS-validated JWTs with no code to maintain. It integrates natively with API Gateway's authorizer. The service holds a GitLab token and cannot be open to the public internet.

**3.8 Lambda vs Fargate for the worker.**
Options: Lambda container image (15 min max, 10 GB), ECS Fargate.
Choice: **Lambda for v1; Fargate as the upgrade path.**
Rationale: Lambda's limits are sufficient for any reasonably-sized repo. It scales to zero between jobs. If generation approaches the 15-minute cap on a large monorepo, the same Dockerfile deploys unchanged to Fargate via EventBridge Pipes - the migration is a config change, not a rewrite.

[← README](../README.md) | [← Architecture](./02-architecture.md) | **Design Decisions** | [Next: Well-Architected →](./04-well-architected.md)
