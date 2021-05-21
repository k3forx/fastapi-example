#!/bin/bash

set -x

DIR=$1
kubectl kustomize "${DIR}" | kube-score score - --ignore-test pod-networkpolicy -o ci | grep -v OK
