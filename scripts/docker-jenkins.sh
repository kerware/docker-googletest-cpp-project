#!/usr/bin/env bash
set -euo pipefail

docker compose build jenkins

docker compose up -d jenkins

echo "Jenkins is starting on http://localhost:8080"
echo "Use the Jenkins UI to create a Multibranch Pipeline or Pipeline job based on the repository and Jenkinsfile."
