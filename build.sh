#!/usr/bin/env bash

export CUR_PATH=$(pwd)
export DOCKER_NAME=blog-backend

# 准备打包的版本信息
TIMENOW=`date +%y.%m.%d.%H%M` && \

COMMIT_ID=$(git rev-parse --short=7 HEAD)

TAG=${TIMENOW}_${COMMIT_ID}

echo "building, please wait a few minutes..."
docker build -f ./Dockerfile -t 13508023081@163.com/$DOCKER_NAME:${TAG} .

echo "tagging..."
docker tag $DOCKER_NAME:${TAG} dockerhub.datagrand.com/ifas/$DOCKER_NAME:${TAG}

echo "pushing to repo..."
docker push dockerhub.datagrand.com/ifas/$DOCKER_NAME:${TAG}