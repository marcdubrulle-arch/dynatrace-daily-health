# PowerShell script to configure GitHub Secrets using GitHub CLI
# Requires: GitHub CLI (gh) installed and authenticated
# Reference: https://cli.github.com/

param(
    [string]$Owner = "marcdubrulle-arch",
    [string]$Repo = "dynatrace-daily-health"
)

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "  GitHub Secrets Configuration Script" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is available
$ghAvailable = $null -ne (Get-Command gh -ErrorAction SilentlyContinue)

if (-not $ghAvailable) {
    Write-Host "❌ GitHub CLI (gh) not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install from: https://cli.github.com/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or configure secrets manually:" -ForegroundColor Yellow
    Write-Host "  https://github.com/$Owner/$Repo/settings/secrets/actions" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "✓ GitHub CLI found" -ForegroundColor Green
Write-Host ""

# Verify authentication
try {
    $authStatus = & gh auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Not authenticated with GitHub!" -ForegroundColor Red
        Write-Host "Run: gh auth login" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✓ Authenticated with GitHub" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error checking auth: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Repository: $Owner/$Repo" -ForegroundColor Cyan
Write-Host ""

# Secrets configuration
$secrets = @{
    "DYNATRACE_BASE_URL" = @{
        value = "https://uxw82338.live.dynatrace.com"
        description = "Dynatrace environment base URL"
        optional = $false
    }
    "DYNATRACE_API_TOKEN" = @{
        value = "<YOUR_TOKEN_HERE>"
        description = "Dynatrace API token (from Settings > API tokens)"
        optional = $false
    }
    "EMAIL_TO" = @{
        value = "marc.dubrulle@orange.com"
        description = "Email recipient for reports"
        optional = $true
    }
}

Write-Host "Configuring secrets..." -ForegroundColor Yellow
Write-Host ""

$successCount = 0
$failureCount = 0

foreach ($secretName in $secrets.Keys) {
    $secretData = $secrets[$secretName]
    $optional = if ($secretData.optional) { "(Optional)" } else { "(Required)" }
    
    Write-Host "  [$secretName] $optional"
    Write-Host "    Description: $($secretData.description)"
    
    if ($secretData.value -eq "<YOUR_TOKEN_HERE>") {
        Write-Host "    ⚠️  Placeholder value - enter actual token interactively" -ForegroundColor Yellow
        
        # Prompt user for value
        $userValue = Read-Host "    Enter value for $secretName (or press Enter to skip)"
        
        if ($userValue.Length -eq 0) {
            if ($secretData.optional) {
                Write-Host "    ⊘ Skipped (optional)" -ForegroundColor Gray
                continue
            }
            else {
                Write-Host "    ✗ Required secret cannot be skipped!" -ForegroundColor Red
                $failureCount++
                continue
            }
        }
        $secretValue = $userValue
    }
    else {
        $secretValue = $secretData.value
    }
    
    try {
        $result = $secretValue | gh secret set $secretName 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    ✓ Configured" -ForegroundColor Green
            $successCount++
        }
        else {
            Write-Host "    ✗ Failed: $result" -ForegroundColor Red
            $failureCount++
        }
    }
    catch {
        Write-Host "    ✗ Error: $_" -ForegroundColor Red
        $failureCount++
    }
    
    Write-Host ""
}

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Result: $successCount configured, $failureCount failed" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

if ($failureCount -eq 0) {
    Write-Host "✅ All required secrets configured!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://github.com/$Owner/$Repo/actions" -ForegroundColor Cyan
    Write-Host "  2. Click: 'Daily Dynatrace Health' workflow" -ForegroundColor Cyan
    Write-Host "  3. Click: 'Run workflow' button" -ForegroundColor Cyan
    Write-Host "  4. Monitor: Check logs for success" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}
else {
    Write-Host "❌ Some secrets failed to configure" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Configure manually at:" -ForegroundColor Yellow
    Write-Host "  https://github.com/$Owner/$Repo/settings/secrets/actions" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
