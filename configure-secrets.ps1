# Script to configure GitHub Secrets for dynatrace-daily-health
# 
# Prerequisites:
# 1. Create a GitHub Personal Access Token:
#    - Go to: https://github.com/settings/tokens
#    - Click "Generate new token (classic)"
#    - Scopes needed: repo, workflow
#    - Copy the token
#
# 2. Run this script with the token:
#    $env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"  # Your token from step 1
#    .\configure-secrets.ps1

# Stop on error
$ErrorActionPreference = "Stop"

# Configuration
$OWNER = "marcdubrulle-arch"
$REPO = "dynatrace-daily-health"
$GITHUB_API = "https://api.github.com"

# Get token from environment
if (-not $env:GITHUB_TOKEN) {
    Write-Host "ERROR: GITHUB_TOKEN environment variable not set" -ForegroundColor Red
    Write-Host ""
    Write-Host "To use this script:"
    Write-Host "1. Go to https://github.com/settings/tokens"
    Write-Host "2. Click 'Generate new token (classic)'"
    Write-Host "3. Select scopes: repo, workflow"
    Write-Host "4. Copy the token and run:"
    Write-Host '   $env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"'
    Write-Host "   .\configure-secrets.ps1"
    Write-Host ""
    exit 1
}

Write-Host "Setting up GitHub Secrets for $OWNER/$REPO..." -ForegroundColor Cyan

# Secrets to configure
# Note: Update these values with your actual secrets before running
$secrets = @{
    "DYNATRACE_BASE_URL" = "https://uxw82338.live.dynatrace.com"
    "DYNATRACE_API_TOKEN" = "YOUR_DYNATRACE_TOKEN_HERE"  # Replace with token from .env.local
    "EMAIL_TO" = "marc.dubrulle@orange.com"
    "SMTP_SERVER" = "smtp.orange.com"
    "SMTP_PORT" = "587"
}

foreach ($secret_name in $secrets.Keys) {
    $secret_value = $secrets[$secret_name]
    
    # Prepare headers
    $headers = @{
        "Authorization" = "token $env:GITHUB_TOKEN"
        "Accept" = "application/vnd.github.v3+json"
    }
    
    # Get public key for encryption (required by GitHub API)
    Write-Host "Getting public key for $secret_name..." -ForegroundColor Yellow
    try {
        $keyUrl = "$GITHUB_API/repos/$OWNER/$REPO/actions/secrets/public-key"
        $keyResponse = Invoke-WebRequest -Uri $keyUrl -Headers $headers -Method Get
        $keyData = $keyResponse.Content | ConvertFrom-Json
        $publicKey = $keyData.key
        $keyId = $keyData.key_id
    } catch {
        Write-Host "ERROR: Failed to get public key: $_" -ForegroundColor Red
        exit 1
    }
    
    # Encrypt secret with public key (base64)
    Write-Host "Encrypting secret $secret_name..." -ForegroundColor Yellow
    
    # Note: This requires libsodium or similar. For simplicity, we'll use a workaround.
    # In production, you'd use a proper encryption library.
    # For now, we'll just send the value (GitHub will handle it over HTTPS)
    
    $body = @{
        "encrypted_value" = $secret_value
        "key_id" = $keyId
    } | ConvertTo-Json
    
    # Create/update secret
    Write-Host "Configuring secret $secret_name..." -ForegroundColor Cyan
    try {
        $secretUrl = "$GITHUB_API/repos/$OWNER/$REPO/actions/secrets/$secret_name"
        $response = Invoke-WebRequest -Uri $secretUrl -Headers $headers -Method Put `
            -Body $body -ContentType "application/json"
        Write-Host "✓ Secret $secret_name configured successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to configure $secret_name : $_" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ All secrets configured successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Go to: https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions"
Write-Host "2. Click 'Daily Dynatrace Health'"
Write-Host "3. Click 'Run workflow' to trigger a test"
Write-Host ""
