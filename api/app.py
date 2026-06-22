"""
Submit / Status Lambda (zip).

Behind API Gateway with a Cognito JWT authorizer:
  POST /orientations            -> submit a project; returns {jobId, status}
  GET  /orientations/{jobId}    -> return job status and, when READY, the report URL

This function never calls GitLab. On a cache miss it enqueues a job on SQS; the
container worker does the heavy lifting. That keeps the API fast and cheap.
"""

import json
import os
import time
import uuid

import boto3

JOBS_TABLE = os.environ["JOBS_TABLE"]
QUEUE_URL = os.environ["QUEUE_URL"]
REPORTS_DOMAIN = os.environ.get("REPORTS_DOMAIN", "")  # CloudFront domain for report links

ddb = boto3.resource("dynamodb").Table(JOBS_TABLE)
sqs = boto3.client("sqs")


def _resp(status: int, body) -> dict:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body),
    }


def _report_url(report_key: str) -> str:
    return f"https://{REPORTS_DOMAIN}/{report_key}" if REPORTS_DOMAIN else report_key


def submit(body: dict) -> dict:
    project = (body.get("project") or "").strip().strip("/")
    # Basic validation: GitLab paths look like "group/subgroup/project".
    if not project or " " in project or not all(part for part in project.split("/")):
        return _resp(400, {"error": "Provide a valid project path, e.g. group/project"})

    # Cache check: has this project already been generated recently?
    cached = ddb.get_item(Key={"PK": f"CACHE#{project}"}).get("Item")
    if cached and cached.get("reportKey"):
        return _resp(200, {
            "jobId": cached["jobId"],
            "status": "READY",
            "cached": True,
            "reportUrl": _report_url(cached["reportKey"]),
        })

    job_id = uuid.uuid4().hex[:12]
    now = int(time.time())
    ddb.put_item(Item={
        "PK": f"JOB#{job_id}",
        "project": project,
        "status": "PENDING",
        "createdAt": now,
    })
    sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps({"jobId": job_id, "project": project}))
    return _resp(202, {"jobId": job_id, "status": "PENDING"})


def status(job_id: str) -> dict:
    item = ddb.get_item(Key={"PK": f"JOB#{job_id}"}).get("Item")
    if not item:
        return _resp(404, {"error": "job not found"})
    out = {"jobId": job_id, "status": item.get("status"), "project": item.get("project")}
    if item.get("status") == "READY" and item.get("reportKey"):
        out["reportUrl"] = _report_url(item["reportKey"])
    if item.get("status") == "FAILED":
        out["error"] = item.get("errorMessage")
    return _resp(200, out)


def handler(event: dict, _context) -> dict:
    method = event.get("httpMethod", "")
    if method == "POST":
        try:
            body = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return _resp(400, {"error": "Invalid JSON body"})
        return submit(body)
    if method == "GET":
        job_id = (event.get("pathParameters") or {}).get("jobId")
        if not job_id:
            return _resp(400, {"error": "jobId is required"})
        return status(job_id)
    return _resp(405, {"error": f"Method {method} not allowed"})
