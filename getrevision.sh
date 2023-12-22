#!/bin/sh
TAG=$(git describe --dirty --always --tags)
SHA=$(git log -1 --pretty=format:"%h" ./ | cut -b -4)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "${BRANCH}" = "master" ]; then
    echo ${TAG}
else
    echo ${TAG}_${BRANCH}
fi
