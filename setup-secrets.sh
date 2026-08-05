#!/bin/bash
# Setup GitHub Secrets for dynatrace-daily-health
# 
# Usage:
#   chmod +x setup-secrets.sh
#   ./setup-secrets.sh
#
# Requires:
#   - GitHub CLI (gh) installed and authenticated
#   - jq (JSON query tool)
#

set -e

REPO="marcdubrulle-arch/dynatrace-daily-health"

echo "🔧 Configuration des Secrets GitHub pour: $REPO"
echo ""

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) n'est pas installé."
    echo "   Installez-le via: https://cli.github.com"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Vous n'êtes pas authentifié auprès de GitHub."
    echo "   Exécutez: gh auth login"
    exit 1
fi

echo "📝 Entrez les informations de configuration:"
echo ""

# Dynatrace Configuration
echo "=== DYNATRACE ==="
read -p "Dynatrace Base URL (ex: https://uxw82338.live.dynatrace.com): " DYNATRACE_BASE_URL
read -s -p "Dynatrace API Token: " DYNATRACE_API_TOKEN
echo ""

# Email Configuration
echo ""
echo "=== EMAIL CONFIGURATION (optionnel) ==="
read -p "SMTP Server (ex: smtp.gmail.com): " SMTP_SERVER
read -p "SMTP Port (ex: 587): " SMTP_PORT
read -p "SMTP User: " SMTP_USER
read -s -p "SMTP Password: " SMTP_PASSWORD
echo ""
read -p "Email From (ex: votre.email@gmail.com): " EMAIL_FROM
read -p "Email To (ex: marc.dubrulle@orange.com): " EMAIL_TO

echo ""
echo "📤 Ajout des secrets à GitHub..."
echo ""

# Add Dynatrace Secrets
gh secret set DYNATRACE_BASE_URL --body "$DYNATRACE_BASE_URL" --repo "$REPO"
echo "✓ DYNATRACE_BASE_URL ajouté"

gh secret set DYNATRACE_API_TOKEN --body "$DYNATRACE_API_TOKEN" --repo "$REPO"
echo "✓ DYNATRACE_API_TOKEN ajouté"

# Add Email Secrets (if provided)
if [ -n "$SMTP_SERVER" ]; then
    gh secret set SMTP_SERVER --body "$SMTP_SERVER" --repo "$REPO"
    echo "✓ SMTP_SERVER ajouté"
    
    gh secret set SMTP_PORT --body "$SMTP_PORT" --repo "$REPO"
    echo "✓ SMTP_PORT ajouté"
    
    gh secret set SMTP_USER --body "$SMTP_USER" --repo "$REPO"
    echo "✓ SMTP_USER ajouté"
    
    gh secret set SMTP_PASSWORD --body "$SMTP_PASSWORD" --repo "$REPO"
    echo "✓ SMTP_PASSWORD ajouté"
    
    gh secret set EMAIL_FROM --body "$EMAIL_FROM" --repo "$REPO"
    echo "✓ EMAIL_FROM ajouté"
    
    gh secret set EMAIL_TO --body "$EMAIL_TO" --repo "$REPO"
    echo "✓ EMAIL_TO ajouté"
else
    echo "⚠️  Email non configuré"
fi

echo ""
echo "✅ Configuration terminée!"
echo ""
echo "Vérifiez les secrets sur:"
echo "   https://github.com/$REPO/settings/secrets/actions"
echo ""
echo "Pour tester le workflow:"
echo "   https://github.com/$REPO/actions/workflows/daily-health.yml"
echo "   Cliquez sur 'Run workflow' → 'Run workflow'"
