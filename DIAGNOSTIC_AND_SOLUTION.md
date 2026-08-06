# Problème d'API Dynatrace - Diagnostic et Solution

## Situation Actuelle

**Date:** August 6, 2026  
**Statut:** ❌ Tous les runs échouent  
**Cause Probable:** Le secret `DYNATRACE_API_TOKEN` n'est pas configuré dans GitHub

## Analyse des Erreurs

### Runs #1-4: HTTP 403 Forbidden
- **Erreur:** Dynatrace API returns 403
- **Cause:** Token invalide, expiré, ou sans permissions
- **Status:** Ne reproduit plus

### Runs #5-7: Process Exit Code 1 (10-20 secondes)
- **Erreur:** "Process completed with exit code 1"
- **Cause Probable:** `ValueError: DYNATRACE_API_TOKEN is required`
- **Raison:** Le secret DYNATRACE_API_TOKEN est vide ou manquant dans GitHub
- **Status:** PROBLEM PERSISTS

### Runs #8-10: YAML Syntax Error
- **Erreur:** "Invalid workflow file: .github/workflows/daily-health.yml#L25"
- **Cause:** Tentative d'ajouter un diagnostic step trop complexe
- **Status:** Résolu dans Run #11

## Solution: Configurer GitHub Secrets Correctement

### Étape 1: Accéder à la Page des Secrets

1. Allez à: https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions

2. Vous devriez voir une liste vide (ou avec des secrets existants)

### Étape 2: Créer le Secret DYNATRACE_API_TOKEN

Si la page retourne 404:
- Attendez quelques minutes (le site peut être temporairement inaccessible)
- Essayez à partir d'une autre navigateur
- Essayez avec incognito mode

Si elle fonctionne:
1. Cliquez sur **"New repository secret"**
2. Nom: `DYNATRACE_API_TOKEN`
3. Valeur: Collez votre token Dynatrace valide
4. Cliquez sur **"Add secret"**

### Étape 3: Créer d'Autres Secrets (Optionnels mais Recommandés)

Pour chaque secret suivant, répétez la même procédure:

| Secret | Valeur |
|--------|--------|
| DYNATRACE_BASE_URL | `https://uxw82338.live.dynatrace.com` |
| SMTP_SERVER | `smtp.orange.com` |
| SMTP_PORT | `587` |
| EMAIL_TO | `marc.dubrulle@orange.com` |

### Étape 4: Vérifier que les Secrets Sont Configurés

Retournez à la page secrets et vérifiez:
- ✓ DYNATRACE_API_TOKEN (avec la date du dernier update)
- ✓ DYNATRACE_BASE_URL
- ✓ SMTP_SERVER
- ✓ SMTP_PORT
- ✓ EMAIL_TO

## Test: Déclencher Manuellement un Nouveau Run

1. Allez à: https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions

2. Cliquez sur **"Daily Dynatrace Health"** workflow

3. Cliquez sur **"Run workflow"**

4. Sélectionnez **"main"** branch

5. Cliquez sur **"Run workflow"**

6. Attendez 2-3 minutes pour voir le résultat

## Vérification du Résultat

### ✅ Succès (Attendu)
- Status: ✓ Success
- Duration: 30-60 secondes
- Un email a été envoyé à marc.dubrulle@orange.com

### ❌ Échec: "Process exit code 1"
- **Cause:** DYNATRACE_API_TOKEN est toujours vide
- **Solution:** Vérifiez à nouveau que vous avez collé correctement le token
- **Note:** Le token doit commencer par `dt0c01.` et avoir +150 caractères

### ❌ Échec: "403 Forbidden"
- **Cause:** Token invalide ou sans permissions Dynatrace
- **Solution:** Vérifiez que le token a les permissions:
  - `entities.read`
  - `problems.read`
  - `metrics.read`
- **Action:** Régénérez un nouveau token dans Dynatrace

### ❌ Échec: "SMTP Error"
- **Cause:** Email n'a pas pu être envoyé
- **Solution:** Vérifiez SMTP_SERVER et les identifiants

## Dépannage: Si GitHub UI Retourne 404

Si vous ne pouvez pas accéder à la page des secrets via le web:

### Option 1: Utiliser GitHub CLI

```bash
# Installer GitHub CLI si nécessaire
# Windows: winget install github-cli
# macOS: brew install gh
# Linux: apt/dnf install gh

# Se connecter à GitHub
gh auth login

# Créer le secret
gh secret set DYNATRACE_API_TOKEN -R marcdubrulle-arch/dynatrace-daily-health

# Vous serez invité à entrer la valeur du token
# Collez votre token Dynatrace ici

# Vérifier que c'est configuré
gh secret list -R marcdubrulle-arch/dynatrace-daily-health
```

### Option 2: Utiliser l'API GitHub

```bash
# Générer un token GitHub personnalisé avec "repo" et "admin:org_hook" permissions

export GH_TOKEN=<votre-github-token>
export REPO_NAME="marcdubrulle-arch/dynatrace-daily-health"
export SECRET_NAME="DYNATRACE_API_TOKEN"
export SECRET_VALUE="<votre-token-dynatrace>"

curl -X PUT \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/$REPO_NAME/actions/secrets/$SECRET_NAME" \
  -d "{\"encrypted_value\": \"$SECRET_VALUE\"}"
```

## Support

Si vous avez des problèmes:

1. **Vérifiez les logs du workflow:**
   - Allez à https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions
   - Cliquez sur le dernier run
   - Cliquez sur le job "report"
   - Cherchez les messages d'erreur

2. **Vérifiez le token Dynatrace:**
   - Allez à https://uxw82338.live.dynatrace.com
   - Accédez à Settings → API Tokens
   - Vérifiez que le token existe et n'est pas expiré

3. **Contactez le support GitHub:**
   - Si les pages retournent 404 ou sont inaccessibles
   - Support GitHub peut vérifier l'état de votre organisation

---

**Dernière mise à jour:** August 6, 2026 10:35 UTC
