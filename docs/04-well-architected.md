[← README](../README.md) | [← Design Decisions](./03-design-decisions.md) | **Well-Architected** | [Next: Risks →](./05-risks.md)

# 4. Well-Architected Framework

| Pillar | How this architecture addresses it |
|---|---|
| **Operational Excellence** | SAM IaC - reproducible deploy and one-command teardown. ECR-versioned worker image. CloudWatch alarms on DLQ depth, Lambda errors, and API latency. X-Ray tracing end-to-end. DLQ preserves failed jobs for inspection. |
| **Security** | WAF managed rules + rate-limiting at the edge. Cognito JWT authorizer - no unauthenticated API access. GitLab token in Secrets Manager, readable only by the worker IAM role, never in the image or env files. Least-privilege IAM role per Lambda. KMS encryption at rest for S3, DynamoDB, SQS, and the secret. Private S3 buckets via CloudFront OAC only. CloudTrail auditing. |
| **Reliability** | SQS decouples submission from generation - a slow worker never blocks the API. SQS visibility timeout retries transient failures. DLQ captures persistent failures. Lambda, API Gateway, SQS, DynamoDB, and S3 are all managed multi-AZ. All job state in DynamoDB/S3, so any Lambda invocation handles any job. |
| **Performance Efficiency** | DynamoDB cache eliminates repeat worker runs - cache hit is instant with no GitLab call. Lambda + SQS scale out automatically with job volume. CloudFront serves UI and reports from edge locations. |
| **Cost Optimization** | Every component bills on use only - Lambda, API Gateway, SQS, DynamoDB (on-demand), S3, SNS. No EC2, no always-on container, no NAT Gateway. Demo cost under $3. DynamoDB cache is the biggest cost lever: popular repos are computed once. |
| **Sustainability** | Scale-to-zero - no idle hardware. Cache eliminates redundant compute. DynamoDB TTL expires stale records, limiting storage growth. All on AWS's high-efficiency managed fleet. |

[← README](../README.md) | [← Design Decisions](./03-design-decisions.md) | **Well-Architected** | [Next: Risks →](./05-risks.md)
