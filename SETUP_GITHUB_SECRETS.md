# Résolution du Problème d'API Dynatrace - Token Non Configuré

## Diagnostic Rapide

Le workflow échoue avec "Process exit code 1" car le secret `DYNATRACE_API_TOKEN` n'est pas enregistré dans GitHub, ou il est vide.

**Signes:**
- Run #5-7 échouent rapidement (10-20 secondes)
- Erreur: "Process completed with exit code 1"
- Probable cause: `ValueError: DYNATRACE_API_TOKEN is required` (non visible dans les logs)

## Solution: Configurer les Secrets GitHub

### Via Interface Web (Recommandé)

1. Allez à: `https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions`

2. Cliquez sur "New repository secret"

3. Ajoutez ces secrets:

   **Secret 1: DYNATRACE_BASE_URL**
   - Name: `DYNATRACE_BASE_URL`
   - Value: `https://uxw82338.live.dynatrace.com`
   - Important: utilisez le domaine `*.live.dynatrace.com` (pas `*.apps.dynatrace.com`)
   - Click "Add secret"

   **Secret 2: DYNATRACE_API_TOKEN**
   - Name: `DYNATRACE_API_TOKEN`
   - Value: `<VOTRE_TOKEN_DYNATRACE>` (Voir les instructions dans la description)
   - Click "Add secret"

   **Secret 3: SMTP_SERVER** (optionnel)
   - Name: `SMTP_SERVER`
   - Value: `smtp.orange.com`
   - Click "Add secret"

   **Secret 4: SMTP_PORT** (optionnel)
   - Name: `SMTP_PORT`
   - Value: `587`
   - Click "Add secret"

   **Secret 5: EMAIL_TO** (optionnel)
   - Name: `EMAIL_TO`
   - Value: `marc.dubrulle@orange.com`
   - Click "Add secret"

### Via Ligne de Commande (Si Web UI ne fonctionne pas)

```bash
# Installer GitHub CLI si nécessaire
# winget install github-cli

gh auth login
cd C:\Users\WHDD0146\dynatrace-daily-health

# Créer les secrets
gh secret set DYNATRACE_BASE_URL --body "https://uxw82338.live.dynatrace.com"
gh secret set DYNATRACE_API_TOKEN --body "<VOTRE_TOKEN_DYNATRACE>"
gh secret set SMTP_SERVER --body "smtp.orange.com"
gh secret set SMTP_PORT --body "587"
gh secret set EMAIL_TO --body "marc.dubrulle@orange.com"

# Vérifier les secrets
gh secret list
```

### Vérifier que les Secrets sont Configurés

1. Allez à la page des secrets: https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions

2. Vous devriez voir:
   - DYNATRACE_API_TOKEN ✓
   - DYNATRACE_BASE_URL ✓
   - SMTP_SERVER ✓
   - SMTP_PORT ✓
   - EMAIL_TO ✓

## Après Avoir Configuré les Secrets

1. Déclenchez manuellement un nouveau workflow:
   - Allez à: https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions
   - Cliquez sur "Daily Dynatrace Health"
   - Cliquez sur "Run workflow"
   - Sélectionnez "main" branch
   - Cliquez sur "Run workflow"

2. Attendez 1-2 minutes pour l'exécution

3. Vérifiez le résultat:
   - ✓ Status: Success
   - ✓ Un email a été envoyé à marc.dubrulle@orange.com

## Dépannage

### Si le Token est Invalide
- Erreur: HTTP 403 Forbidden
- Solution: Vérifiez que le token Dynatrace a les permissions:
  - `entities.read`
  - `problems.read`
  - `metrics.read`

### Si les Variables d'Environnement Sont Vides
- Erreur: "ValueError: DYNATRACE_API_TOKEN is required"
- Solution: Assurez-vous que tous les secrets sont enregistrés dans GitHub

### Si l'Email n'est pas Envoyé
- Vérifiez que SMTP_SERVER et EMAIL_TO sont configurés
- Vérifiez les logs pour les erreurs SMTP

## Test Local

Avant de configurer GitHub, testez localement:

```bash
# Windows PowerShell
$env:DYNATRACE_BASE_URL="https://uxw82338.live.dynatrace.com"
$env:DYNATRACE_API_TOKEN="<VOTRE_TOKEN_DYNATRACE>"
$env:EMAIL_TO="marc.dubrulle@orange.com"

python run_daily.py
```

---

**Dernière mise à jour:** August 6, 2026
