# 🚀 Configuration et Test du Workflow Dynatrace

## ✅ Nouveau Token Dynatrace Disponible

Tu as un nouveau token Dynatrace avec les bons scopes:
- ✅ entities.read
- ✅ metrics.read  
- ✅ problems.read
- ✅ credentialVault.read

---

## Option 1: Configuration Manuelle via GitHub UI (30 secondes)

**Étapes:**

1. **Ouvrir les paramètres des secrets:**
   - https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions

2. **Créer Secret: DYNATRACE_BASE_URL**
   - Click "New repository secret"
   - Name: `DYNATRACE_BASE_URL`
   - Value: `https://uxw82338.live.dynatrace.com`
   - Click "Add secret"

3. **Créer Secret: DYNATRACE_API_TOKEN**
   - Click "New repository secret"
   - Name: `DYNATRACE_API_TOKEN`
   - Value: (Copier le token que tu as reçu)
   - Click "Add secret"

4. **Créer Secret: EMAIL_TO** (optionnel)
   - Click "New repository secret"
   - Name: `EMAIL_TO`
   - Value: `marc.dubrulle@orange.com`
   - Click "Add secret"

---

## Option 2: Configuration via GitHub CLI

Si tu as `gh` (GitHub CLI) installé:

```bash
# Set the base URL secret
gh secret set DYNATRACE_BASE_URL --body "https://uxw82338.live.dynatrace.com"

# Set the API token (replace <TOKEN> with your actual token)
gh secret set DYNATRACE_API_TOKEN --body "<YOUR_DYNATRACE_TOKEN>"

# Set email (optional)
gh secret set EMAIL_TO --body "marc.dubrulle@orange.com"
```

---

## Option 3: Test Local

Pour tester le code en local avant de pousser:

```bash
# Ensure .env.local exists with your token
cat .env.local

# Run the workflow
python run_daily.py
```

---

## Déclencher le Workflow sur GitHub

Une fois les secrets configurés:

1. **Aller à Actions:**
   https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions

2. **Sélectionner le workflow:**
   Click sur "Daily Dynatrace Health"

3. **Déclencher un test:**
   - Click "Run workflow" button
   - Select branch: `main`
   - Click "Run workflow"

---

## ✅ Vérification Attendue

Le workflow devrait:
- ✅ Checkout code
- ✅ Setup Python 3.12
- ✅ Install dependencies
- ✅ Run daily report
- ✅ Generate report
- ✅ Upload artifacts

**Logs à vérifier:**
- `DEBUG: DYNATRACE_BASE_URL = '***'` (masked)
- `DEBUG: DYNATRACE_API_TOKEN = '****...'` (masked)
- `Fetching problems from last 24h...`
- `Generating report...`
- `✓ Report saved to reports/report_*.md`

---

## 🔧 Si ça échoue

| Erreur | Cause | Solution |
|--------|-------|----------|
| `CONFIG ERROR: DYNATRACE_BASE_URL is required` | Secrets non configurés | Configurer les secrets dans GitHub Settings |
| `401 Unauthorized` | Token invalide/expiré | Générer un nouveau token Dynatrace |
| `400 Bad Request` | Paramètres API incorrects | Vérifier les sélecteurs de problèmes |
| `Cannot send email` | Paramètres SMTP manquants | Optionnel - ajouter SMTP si souhaité |

---

## 📋 Checklist

- [ ] Token Dynatrace généré avec les bons scopes
- [ ] Secrets configurés dans GitHub Settings
- [ ] Base URL: `https://uxw82338.live.dynatrace.com`
- [ ] Workflow déclenché manuellement
- [ ] Logs vérifiés pour les erreurs
- [ ] Rapport généré dans les artifacts

**Status:** Ready to configure! 🚀
