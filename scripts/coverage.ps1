$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path reports/coverage | Out-Null
docker compose run --rm coverage
Write-Host "Rapport de couverture : reports/coverage/index.html"
