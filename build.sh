#!/usr/bin/env bash

export CUR_PATH=$(pwd)
export DOCKER_NAME=tsurol/blog

# 准备打包的版本信息
TIMENOW=`date +%y.%m.%d.%H%M` && \

COMMIT_ID=$(git rev-parse --short=7 HEAD)

TAG=${TIMENOW}_${COMMIT_ID}

echo "building, please wait a few minutes..."
docker build -f ./Dockerfile -t $DOCKER_NAME:${TAG} .

echo "tagging..."
docker tag $DOCKER_NAME:${TAG} $DOCKER_NAME:${TAG}

echo "pushing to repo..."
docker push $DOCKER_NAME:${TAG}