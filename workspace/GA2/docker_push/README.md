This folder contains a small helper script to push the locally built Docker image to Docker Hub.

Steps to use (Git Bash):

1. Build the image locally (from repository root):

```bash
python build_and_run.py
# or
# docker build -t ga2-25c816:latest .
```

2. Edit the script or set environment variables:

```bash
export DOCKER_USER=your-dockerhub-username
export DOCKER_REPO=ga2-25c816
```

3. Run the helper script:

```bash
cd workspace/GA2/docker_push
chmod +x push_image.sh
./push_image.sh
```

The script will tag the local image as `${DOCKER_USER}/${DOCKER_REPO}:22f3002579` and push it to Docker Hub. After push, visit:

`https://hub.docker.com/repository/docker/${DOCKER_USER}/${DOCKER_REPO}/general`

If you prefer, create the repository on Docker Hub UI first and set visibility to Public.
