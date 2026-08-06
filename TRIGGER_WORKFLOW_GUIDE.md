# Guide: Déclencher le Workflow Dynatrace Daily Health

Vous avez configuré `DYNATRACE_API_TOKEN` dans GitHub Secrets ✅

Maintenant, il faut **déclencher un test du workflow** pour vérifier que tout fonctionne.

## Option 1: Via l'Interface Web GitHub (Recommandé - Plus facile)

### Étapes:

1. **Allez à GitHub Actions:**
   - https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions

2. **Cliquez sur le workflow "Daily Dynatrace Health":**
   - C'est le workflow le plus à gauche

3. **Cherchez le bouton "Run workflow" (devrait être en haut à droite)**
   - S'il n'est pas visible immédiatement, essayez:
     - Cliquez sur le bouton "..." (trois points) en haut à droite
     - Sélectionnez "Run workflow"

4. **Une fois le modal d'exécution ouvert:**
   - Vérifiez que la branche est définie à "main"
   - Cliquez "Run workflow"

5. **Attendez que le workflow s'exécute (environ 2-3 minutes)**
   - Vous verrez le statut changer de "Queued" → "In progress" → "Completed"

---

## Option 2: Via GitHub CLI (Si vous avez `gh` installé)

```bash
# Configuration initiale (une seule fois)
gh auth login
# Sélectionnez GitHub.com, puis "HTTPS", puis "Authenticate with a token from..."

# Déclencher le workflow
gh workflow run daily-health.yml --repo marcdubrulle-arch/dynatrace-daily-health

# Voir les derniers runs
gh run list --repo marcdubrulle-arch/dynatrace-daily-health --limit 5
```

---

## Option 3: Via Script PowerShell (Windows)

Ce script utilise l'API GitHub directement:

### 3a. Obtenir un GitHub Personal Access Token

1. **Allez à:** https://github.com/settings/tokens

2. **Cliquez sur "Generate new token (classic)"**

3. **Configurez le token:**
   - **Token name:** "Dynatrace Workflow Trigger"
   - **Scopes à sélectionner:**
     - ✅ `repo` (full access)
     - ✅ `workflow` 
   - **Note:** Gardez ce token secret!

4. **Cliquez "Generate token"**

5. **Copiez le token** (vous ne pourrez le voir qu'une fois)

### 3b. Exécuter le Script PowerShell

```powershell
# Méthode 1: Passer le token en paramètre
.\trigger-workflow.ps1 -GitHubToken "ghp_xxxxxxxxxxxx"

# Méthode 2: Définir la variable d'environnement
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"
.\trigger-workflow.ps1

# Méthode 3: Définir pour toute la session
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"
.\trigger-workflow.ps1
.\verify_setup.py
```

---

## Option 4: Via cURL (Ligne de commande)

```bash
# Définissez votre token
GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# Déclenchez le workflow
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/marcdubrulle-arch/dynatrace-daily-health/actions/workflows/daily-health.yml/dispatches" \
  -d '{"ref":"main"}'

# Attendez 5 secondes
sleep 5

# Vérifiez les runs
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/marcdubrulle-arch/dynatrace-daily-health/actions/runs?per_page=3" \
  | jq '.workflow_runs[] | {id, name, status, created_at}'
```

---

## Que Vérifier Après l'Exécution

### ✅ Le Workflow Doit Réussir Avec:

1. **Tous les secrets GitHub configurés:**
   - ✅ `DYNATRACE_API_TOKEN` (vous l'avez fait)
   - ✅ `DYNATRACE_BASE_URL`
   - ✅ `SMTP_SERVER` (optionnel mais recommandé)
   - ✅ `SMTP_PORT` (optionnel)
   - ✅ `EMAIL_TO` (optionnel)

2. **Logs du Workflow Montrant:**
   ```
   ✅ Checkout
   ✅ Setup Python
   ✅ Install dependencies
   ✅ Generate report ← Ici, les données Dynatrace seront chargées
   ✅ Upload reports
   ```

3. **Pas d'erreurs comme:**
   - ❌ `ValueError: DYNATRACE_API_TOKEN is required`
   - ❌ `HTTP 403 Forbidden`
   - ❌ `ValueError: invalid literal for int()`

### ✅ Résultats Attendus:

1. **Fichiers générés:** `reports/daily_health_report.md` et `.json`
2. **Email envoyé:** Si SMTP configuré, un email HTML va à `EMAIL_TO`
3. **Logs affichant:** 
   ```
   DEBUG: DYNATRACE_BASE_URL = 'https://uxw82338.live.dynatrace.com'
   DEBUG: DYNATRACE_API_TOKEN length = 180
   DEBUG: Config validation passed
   ```

---

## Troubleshooting

### Le Workflow Échoue?

1. **Cliquez sur le run échoué**
2. **Allez à l'onglet "Logs"**
3. **Cherchez le message d'erreur exact**
4. **Consultez:** [DIAGNOSTIC_AND_SOLUTION.md](DIAGNOSTIC_AND_SOLUTION.md)

### Message d'Erreur: "workflow_dispatch not found"?

Assurez-vous que le fichier `.github/workflows/daily-health.yml` contient:
```yaml
on:
  push:
    branches:
      - main
  schedule:
    - cron: "0 18 * * *"
  workflow_dispatch:  ← Cette ligne doit être présente
```

### Message: "Token invalid or expired"?

1. Vérifiez le token dans GitHub Secrets
2. Vérifiez qu'il a les scopes corrects (`repo`, `workflow`)
3. Régénérez-le si nécessaire

---

## Prochaines Étapes

Après avoir déclenché le workflow avec succès:

1. ✅ Vérifiez que le workflow passe (status = "✅")
2. ✅ Vérifiez les logs pour s'assurer qu'il charge les données Dynatrace
3. ✅ Si email configuré, vérifiez que vous avez reçu l'email
4. ✅ Le workflow s'exécutera automatiquement chaque jour à 18:00 UTC (schedule)

---

## Questions?

Consultez les fichiers suivants:
- `SETUP_GITHUB_SECRETS.md` - Configuration des secrets GitHub
- `DIAGNOSTIC_AND_SOLUTION.md` - Troubleshooting complet
- `CONFIGURATION.md` - Configuration détaillée
