# Configure GitHub Secrets for dynatrace-daily-health
# Usage: ./add-secrets.ps1 -GitHubToken "your_token_here"

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubToken,
    
    [string]$Owner = "marcdubrulle-arch",
    [string]$Repo = "dynatrace-daily-health"
)

$baseUrl = "https://api.github.com/repos/$Owner/$Repo/actions/secrets"
$headers = @{
    "Authorization" = "Bearer $GitHubToken"
    "Accept" = "application/vnd.github.v3+json"
    "Content-Type" = "application/json"
}

function Add-Secret {
    param(
        [string]$Name,
        [string]$Value
    )
    
    $body = @{
        encrypted_value = $Value
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/$Name" -Method PUT -Headers $headers -Body $body
        Write-Host "✓ $Name added successfully" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "✗ Failed to add $Name : $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Secrets to add
$secrets = @{
    "DYNATRACE_BASE_URL" = "https://uxw82338.live.dynatrace.com"
    "DYNATRACE_API_TOKEN" = "YOUR_DYNATRACE_TOKEN_HERE"  # Replace with actual token
    "EMAIL_TO" = "marc.dubrulle@orange.com"
}

Write-Host "🔐 Adding secrets to $Owner/$Repo..." -ForegroundColor Cyan
Write-Host ""

$success = 0
$failed = 0

foreach ($name in $secrets.Keys) {
    if (Add-Secret -Name $name -Value $secrets[$name]) {
        $success++
    } else {
        $failed++
    }
}

Write-Host ""
Write-Host "📊 Summary: $success added, $failed failed" -ForegroundColor Yellow
Write-Host ""
Write-Host "✅ Secrets configured! Check them at:" -ForegroundColor Green
Write-Host "   https://github.com/$Owner/$Repo/settings/secrets/actions"
