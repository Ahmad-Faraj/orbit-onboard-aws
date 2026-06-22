"""
Orientation Worker Lambda (container image).

Triggered by SQS. For each job it:
  1. Reads the GitLab token from Secrets Manager and configures glab.
  2. Runs the bundled `orbit-onboard` CLI for the requested project, capturing the
     rendered orientation (Markdown, including the Mermaid architecture diagram).
  3. Writes the report to the S3 reports bucket.
  4. Updates the job to READY in DynamoDB (and refreshes the cache entry).
  5. Publishes a completion message to SNS.

A job that raises is left for SQS to retry; after maxReceiveCount it lands in the DLQ.

This is a reference implementation — harden error handling and add the latest-commit
cache key before production use.
"""

import json
import os
import subprocess
import time

import boto3

REPORTS_BUCKET = os.environ["REPORTS_BUCKET"]
JOBS_TABLE = os.environ["JOBS_TABLE"]
SECRET_ID = os.environ["GITLAB_SECRET_ID"]
TOPIC_ARN = os.environ.get("COMPLETION_TOPIC_ARN", "")
CACHE_TTL_DAYS = int(os.environ.get("CACHE_TTL_DAYS", "7"))

CLI_PATH = os.path.join(os.environ.get("LAMBDA_TASK_ROOT", "."), "orbit-onboard")

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb").Table(JOBS_TABLE)
sns = boto3.client("sns")
secrets = boto3.client("secretsmanager")

_token_cache = None


def gitlab_token() -> str:
    """Fetch (and cache for the container's lifetime) the GitLab token."""
    global _token_cache
    if _token_cache is None:
        value = secrets.get_secret_value(SecretId=SECRET_ID)["SecretString"]
        try:
            _token_cache = json.loads(value).get("token", value)
        except json.JSONDecodeError:
            _token_cache = value
    return _token_cache


def generate_orientation(project_path: str) -> str:
    """Run the bundled CLI and return its Markdown output."""
    env = dict(os.environ)
    env["GITLAB_TOKEN"] = gitlab_token()  # glab reads GITLAB_TOKEN
    env["HOME"] = "/tmp"                   # glab needs a writable HOME for its config

    proc = subprocess.run(
        ["python3", CLI_PATH, project_path],
        capture_output=True,
        text=True,
        env=env,
        timeout=600,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "orbit-onboard failed")
    return proc.stdout


def process_job(job: dict) -> None:
    job_id = job["jobId"]
    project = job["project"]

    report_md = generate_orientation(project)
    key = f"reports/{job_id}.md"
    s3.put_object(
        Bucket=REPORTS_BUCKET,
        Key=key,
        Body=report_md.encode("utf-8"),
        ContentType="text/markdown; charset=utf-8",
    )

    now = int(time.time())
    ttl = now + CACHE_TTL_DAYS * 86400

    # Mark the job READY ...
    ddb.update_item(
        Key={"PK": f"JOB#{job_id}"},
        UpdateExpression="SET #s = :s, reportKey = :k, updatedAt = :t",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "READY", ":k": key, ":t": now},
    )
    # ... and refresh the cache pointer for this project.
    ddb.put_item(
        Item={"PK": f"CACHE#{project}", "jobId": job_id, "reportKey": key, "ttl": ttl}
    )

    if TOPIC_ARN:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Orientation ready",
            Message=json.dumps({"jobId": job_id, "project": project, "reportKey": key}),
        )


def handler(event: dict, _context) -> dict:
    for record in event.get("Records", []):
        job = json.loads(record["body"])
        try:
            process_job(job)
        except Exception as exc:  # noqa: BLE001 - mark FAILED, then re-raise for SQS retry/DLQ
            print(json.dumps({"level": "ERROR", "job": job.get("jobId"), "error": str(exc)}))
            try:
                ddb.update_item(
                    Key={"PK": f"JOB#{job['jobId']}"},
                    UpdateExpression="SET #s = :s, errorMessage = :e",
                    ExpressionAttributeNames={"#s": "status"},
                    ExpressionAttributeValues={":s": "FAILED", ":e": str(exc)[:500]},
                )
            except Exception:  # noqa: BLE001
                pass
            raise
    return {"ok": True}
