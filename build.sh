#!/bin/bash

set -eo pipefail

APP_NAME='compev'
GIT_DIR="$(git worktree list | head -n1 | cut -d' ' -f1)"
rev="$(git rev-parse HEAD)"
working_path="$(mktemp -d "/tmp/$APP_NAME-XXX")"
env -u GIT_QUARANTINE_PATH git worktree add "$working_path" "$rev"
echo "Using $working_path as build dir"
find "$working_path" -name '.git' -prune -exec rm -rf {} \;
env -u GIT_QUARANTINE_PATH git worktree prune
trap 'rm -rf "$working_path"' RETURN INT TERM EXIT

container_id=$(docker run -d -v "$GIT_DIR/.cache:/tmp/cache" -v "$working_path:/tmp/app" gliderlabs/herokuish /build)
docker attach "$container_id"
docker wait "$container_id"
docker commit "$container_id" "dokkuish/$APP_NAME"
docker rm "$container_id"
