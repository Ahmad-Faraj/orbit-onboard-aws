[← README](../README.md) | [← Requirements](./01-requirements.md) | **Architecture** | [Next: Design Decisions →](./03-design-decisions.md)

# 2. Architecture

## Components

**EDGE & CDN - CloudFront + WAF + S3**
Static SPA in a private S3 bucket, served only through CloudFront (Origin Access Control). WAF applies managed rule groups and a rate-based rule at the edge before traffic reaches the API.

**AUTH - Cognito**
Cognito User Pool handles sign-up, sign-in, and MFA. It issues JWTs that API Gateway validates on every request - unauthenticated calls are rejected before any Lambda runs.

**API TIER - API Gateway + Submit/Status Lambda**
Two endpoints: `POST /orientations` (submit) and `GET /orientations/{jobId}` (poll status). A zip Lambda backs both - it checks the DynamoDB cache and either returns a cached report or enqueues an SQS job. It never calls GitLab, so it stays fast.

**ASYNC CORE - SQS + Worker Lambda + ECR**
SQS decouples the API from the slower generation work. The Worker Lambda is a **container image** (stored in ECR) because the `glab` binary cannot be shipped in a zip Lambda. On trigger: reads the GitLab token from Secrets Manager → runs Orbit queries → writes the report to S3 → updates DynamoDB to `READY` → publishes to SNS. A Dead-Letter Queue captures messages after max retries.

**DATA - DynamoDB**
Single on-demand table, two item types:
- `JOB#<id>` - status, project, S3 key, timestamps.
- `CACHE#<project>` - report key + TTL for cache expiry.

Zero cost when idle (on-demand billing).

**RESULTS - S3 Reports + SNS**
Reports written to a private S3 bucket, served via CloudFront. SNS publishes a completion event for downstream notification.

**OBSERVABILITY & SECURITY - CloudWatch + X-Ray + KMS + IAM**
CloudWatch logs and metrics from all Lambda functions and SQS; alarms on error rate and DLQ depth. X-Ray traces the full job path. KMS encrypts S3, DynamoDB, SQS, and the secret at rest. Each Lambda has a least-privilege IAM role scoped to named resources.

## Request Flows

**Cache miss (first run)**
```
User → Cognito sign-in → JWT
User → WAF → API Gateway POST /orientations
     → Submit Lambda → DynamoDB (MISS) → SQS enqueue → return jobId

SQS → Worker Lambda (ECR image)
     → Secrets Manager (GitLab token)
     → GitLab Orbit queries
     → S3 write report → DynamoDB READY → SNS notify

User → GET /orientations/{jobId} → READY + report URL
User → CloudFront → S3 report
```

**Cache hit (repeat request)**
```
User → API Gateway POST /orientations
     → Submit Lambda → DynamoDB (HIT) → return report URL immediately
```

[← README](../README.md) | [← Requirements](./01-requirements.md) | **Architecture** | [Next: Design Decisions →](./03-design-decisions.md)
