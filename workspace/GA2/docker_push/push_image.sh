#!/usr/bin/env bash
set -euo pipefail

# Usage: set DOCKER_USER and DOCKER_REPO env vars or edit below
: ${DOCKER_USER:="siddharthmagesh"}
: ${DOCKER_REPO:="ga2-25c816"}
LOCAL_IMAGE="ga2-25c816:latest"
TAG="22f3002579"
REMOTE_IMAGE="${DOCKER_USER}/${DOCKER_REPO}:${TAG}"

if ! docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^${LOCAL_IMAGE}$"; then
  echo "Local image ${LOCAL_IMAGE} not found. Build it first." >&2
  exit 1
fi

echo "Logging in to Docker Hub (interactive)..."
docker login

echo "Tagging ${LOCAL_IMAGE} -> ${REMOTE_IMAGE}"
docker tag "${LOCAL_IMAGE}" "${REMOTE_IMAGE}"

echo "Pushing ${REMOTE_IMAGE}..."
docker push "${REMOTE_IMAGE}"

echo "Done. Docker Hub URL: https://hub.docker.com/repository/docker/${DOCKER_USER}/${DOCKER_REPO}/general"
