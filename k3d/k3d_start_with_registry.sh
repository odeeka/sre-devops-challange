#!/bin/bash

k3d cluster create dev-cluster --config ./dev-cluster-config.yaml --registry-create mycluster-registry

CONTAINER_ID=$(docker ps --filter "name=mycluster-registry" --quiet)

echo "Registry container ID: ${CONTAINER_ID}"

REGISTRY_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "5000/tcp") 0).HostPort}}' $CONTAINER_ID)

echo "K3d local registry => mycluster-registry:${REGISTRY_PORT}"