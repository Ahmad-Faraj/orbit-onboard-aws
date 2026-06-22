# Container image for the Orientation Worker Lambda.
#
# Why a container (not a zip Lambda)? The worker reuses the original orbit-onboard
# CLI, which shells out to the `glab` binary. A container image lets us bake both
# Python and the glab binary into one reproducible artifact stored in Amazon ECR.
#
# Build context must be the REPOSITORY ROOT (so it can copy ./orbit-onboard):
#   docker build -f aws-architecture/worker/Dockerfile -t orbit-onboard-worker .

FROM public.ecr.aws/lambda/python:3.12

# --- install the glab CLI (verify the version/URL against gitlab.com/gitlab-org/cli/-/releases) ---
ARG GLAB_VERSION=1.45.0
RUN dnf install -y tar gzip 2>/dev/null || yum install -y tar gzip
RUN curl -sSL "https://gitlab.com/gitlab-org/cli/-/releases/v${GLAB_VERSION}/downloads/glab_${GLAB_VERSION}_linux_amd64.tar.gz" -o /tmp/glab.tgz \
    && tar -xzf /tmp/glab.tgz -C /tmp \
    && (mv /tmp/bin/glab /usr/local/bin/glab 2>/dev/null || mv /tmp/glab /usr/local/bin/glab) \
    && chmod +x /usr/local/bin/glab \
    && rm -rf /tmp/glab.tgz /tmp/bin

# Python deps for the handler (boto3 is already in the base image).
COPY aws-architecture/worker/requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Bundle the original CLI and the Lambda handler.
COPY orbit-onboard ${LAMBDA_TASK_ROOT}/orbit-onboard
COPY aws-architecture/worker/app.py ${LAMBDA_TASK_ROOT}/app.py
RUN chmod +x ${LAMBDA_TASK_ROOT}/orbit-onboard

CMD ["app.handler"]
