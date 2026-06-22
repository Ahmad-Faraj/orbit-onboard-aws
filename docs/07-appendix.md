[← README](../README.md) | [← Future Work](./06-future-work.md) | **Appendix**

# 7. Appendix

## Service Inventory

| Layer | Service | Role |
|---|---|---|
| Edge | CloudFront | CDN for UI and reports; single public entry point |
| Edge | S3 (UI bucket) | Static SPA hosting |
| Edge | WAF | Managed rules + rate-based rule on CloudFront |
| Auth | Cognito User Pool | Sign-up, sign-in, MFA; issues JWTs |
| API | API Gateway | POST /orientations, GET /orientations/{jobId} |
| Compute | Lambda (zip) | Submit / Status - cache check and job broker |
| Compute | Lambda (container) | Worker - runs glab, generates and stores report |
| Registry | ECR | Worker container image |
| Queue | SQS Job Queue | Async decoupling; visibility timeout for retries |
| Queue | SQS DLQ | Captures jobs exhausting max retries |
| Data | DynamoDB (on-demand) | Job status + orientation cache with TTL |
| Storage | S3 (reports bucket) | Rendered orientation reports |
| Secrets | Secrets Manager | GitLab service-account token |
| Notify | SNS | Completion event |
| Observability | CloudWatch | Logs, metrics, alarms |
| Observability | X-Ray | Distributed tracing |
| Security | KMS | At-rest encryption for S3, DynamoDB, SQS, secret |
| Security | IAM | Least-privilege role per Lambda |
| IaC | AWS SAM | One-command deploy and teardown |

## Deployment

Requires Docker, AWS SAM CLI, and an AWS account.

```bash
# 1. Store the GitLab token
aws secretsmanager create-secret \
  --name orbit-onboard/gitlab-token \
  --secret-string '{"token":"glpat-xxxx"}'

# 2. Build and deploy
cd aws-architecture/infra
sam build
sam deploy --guided   # set GitLabSecretArn when prompted

# 3. Create a test user
aws cognito-idp sign-up --client-id <ClientId> --username you@example.com --password 'Passw0rd!'
aws cognito-idp admin-confirm-sign-up --user-pool-id <PoolId> --username you@example.com
aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH \
  --client-id <ClientId> \
  --auth-parameters USERNAME=you@example.com,PASSWORD='Passw0rd!'

# 4. Submit a job and poll
curl -X POST "<ApiUrl>/orientations" \
  -H "Authorization: <IdToken>" -H "Content-Type: application/json" \
  -d '{"project":"gitlab-org/orbit/knowledge-graph"}'

curl "<ApiUrl>/orientations/<jobId>" -H "Authorization: <IdToken>"

# 5. Tear down
sam delete
aws secretsmanager delete-secret --secret-id orbit-onboard/gitlab-token --force-delete-without-recovery
```

[← README](../README.md) | [← Future Work](./06-future-work.md) | **Appendix**
