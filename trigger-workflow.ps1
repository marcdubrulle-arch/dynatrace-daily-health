#!/usr/bin/env pwsh
<#
.SYNOPSIS
Trigger the Daily Dynatrace Health workflow via GitHub API
.DESCRIPTION
Requires a GitHub Personal Access Token with 'repo' and 'workflow' scopes
.PARAMETER GitHubToken
GitHub Personal Access Token (or set GITHUB_TOKEN env var)
.EXAMPLE
.\trigger-workflow.ps1 -GitHubToken "ghp_xxxxxxxxxxxx"
OR
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"; .\trigger-workflow.ps1
#>

param(
    [string]$GitHubToken
)

# Get token from parameter or environment variable
if (-not $GitHubToken) {
    $GitHubToken = $env:GITHUB_TOKEN
}

if (-not $GitHubToken) {
    Write-Host "❌ Error: GitHub token required" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  1. Set environment variable:"
    Write-Host '     $env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"'
    Write-Host "  2. Run this script: .\trigger-workflow.ps1"
    Write-Host ""
    Write-Host "  OR pass token as parameter:"
    Write-Host '     .\trigger-workflow.ps1 -GitHubToken "ghp_xxxxxxxxxxxx"'
    Write-Host ""
    Write-Host "To get a GitHub token:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://github.com/settings/tokens"
    Write-Host "  2. Click 'Generate new token (classic)'"
    Write-Host "  3. Select scopes: repo (full), workflow"
    Write-Host "  4. Copy the token and use it above"
    exit 1
}

$Owner = "marcdubrulle-arch"
$Repo = "dynatrace-daily-health"
$WorkflowId = "daily-health.yml"

Write-Host "🚀 Triggering workflow: $WorkflowId" -ForegroundColor Cyan
Write-Host ""

$Headers = @{
    "Authorization" = "token $GitHubToken"
    "Accept" = "application/vnd.github.v3+json"
    "Content-Type" = "application/json"
}

$Url = "https://api.github.com/repos/$Owner/$Repo/actions/workflows/$WorkflowId/dispatches"
$Body = @{
    ref = "main"
} | ConvertTo-Json

try {
    $Response = Invoke-WebRequest -Uri $Url -Method POST -Headers $Headers -Body $Body
    Write-Host "✅ Workflow triggered successfully!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ Failed to trigger workflow" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try to show error details
    try {
        $ErrorContent = $_.Exception.Response.Content.ReadAsStringAsync().Result
        Write-Host "Details: $ErrorContent" -ForegroundColor Red
    } catch {}
    
    exit 1
}

Write-Host "Check status at:" -ForegroundColor Yellow
Write-Host "  https://github.com/$Owner/$Repo/actions"
Write-Host ""

# Wait a moment for the workflow to start
Write-Host "Waiting for the workflow to start (5 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Get recent runs
Write-Host "Fetching latest run..." -ForegroundColor Gray
try {
    $RunsUrl = "https://api.github.com/repos/$Owner/$Repo/actions/runs?per_page=5"
    $RunsResponse = Invoke-WebRequest -Uri $RunsUrl -Headers $Headers
    $Runs = $RunsResponse.Content | ConvertFrom-Json
    
    if ($Runs.workflow_runs -and $Runs.workflow_runs.Count -gt 0) {
        $LatestRun = $Runs.workflow_runs[0]
        Write-Host "Latest Run:" -ForegroundColor Yellow
        Write-Host "  ID: $($LatestRun.id)" -ForegroundColor Cyan
        Write-Host "  Name: $($LatestRun.name)" -ForegroundColor Cyan
        Write-Host "  Status: $($LatestRun.status)" -ForegroundColor Cyan
        Write-Host "  Conclusion: $($LatestRun.conclusion)" -ForegroundColor Cyan
        Write-Host "  Created: $($LatestRun.created_at)" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "View at: https://github.com/$Owner/$Repo/actions/runs/$($LatestRun.id)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "Could not fetch run details: $($_.Exception.Message)" -ForegroundColor Gray
}
