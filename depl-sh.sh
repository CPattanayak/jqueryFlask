#!/bin/bash
#
# Script to download and deploy and openwhisk actions
#


COUNT=$(kubectl get pods | grep -c backend-deployment)
while [[ "$COUNT" != 1 ]]; do
 COUNT=$(kubectl get pods | grep -c backend-deployment)
 sleep 5
done
 
