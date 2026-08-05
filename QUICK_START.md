# 🚀 Configuration en 3 Étapes - 5 Minutes!

## Étape 1️⃣ : Ajouter 3 Secrets GitHub

### Lien Direct:
👉 **https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions**

### Pour chaque secret, répète 3 fois:

**PREMIÈRE SECRET:**
1. Clique "New repository secret"
2. **Name:** `DYNATRACE_BASE_URL`
3. **Value:** `https://uxw82338.live.dynatrace.com`
4. Clique "Add secret" ✓

**DEUXIÈME SECRET:**
1. Clique "New repository secret"
2. **Name:** `DYNATRACE_API_TOKEN`
3. **Value:** `dt0c01.xxxxxxxxxxxxx...` (Ton token Dynatrace complet)
4. Clique "Add secret" ✓

**TROISIÈME SECRET:**
1. Clique "New repository secret"
2. **Name:** `EMAIL_TO`
3. **Value:** `marc.dubrulle@orange.com`
4. Clique "Add secret" ✓

---

## Étape 2️⃣ : Tester le Workflow

### Lien Direct:
👉 **https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions/workflows/daily-health.yml**

1. Clique sur le workflow **"Daily Dynatrace Health"**
2. Clique sur le bouton gris "Run workflow"
3. Clique sur "Run workflow" (confirmation)
4. ⏳ Attends 2-5 minutes

---

## Étape 3️⃣ : Vérifier les Résultats

Une fois le workflow lancé:

### Voir les Logs:
- La run s'affiche en bas de la page
- Clique dessus
- Regarde les logs pour voir s'il y a des erreurs

### Télécharger les Rapports:
- Scroller jusqu'à "Artifacts"
- Télécharge "dynatrace-daily-health"
- Ouvre les fichiers `.md` et `.json`

### Vérifier l'Email:
- Cherche un email "[Dynatrace] Daily Health Report"
- Vérifiez spam aussi!

---

## ✅ Comment Confirmer que c'est OK?

Les 3 signes que ça marche:

1. ✓ Pas d'erreurs en rouge dans les logs
2. ✓ Artefacts générés (report_.md et report_.json)
3. ✓ Email reçu (optionnel, voir note ci-dessous)

**Note Email:** Si SMTP n'est pas configuré, l'email ne sera pas envoyé. C'est OK pour le test. Le workflow continue quand même.

---

## 🔧 Si Erreur Dynatrace 403?

Ça veut dire le token n'a pas les bonnes permissions:

1. Allez dans Dynatrace → Settings → Dynatrace API
2. Créez un nouveau token avec les scopes:
   - ✓ `entities.read`
   - ✓ `metrics.read`
   - ✓ `problems.read`
3. Remplacez `DYNATRACE_API_TOKEN` dans GitHub secrets

---

## 📞 Support

Besoin d'aide? Consultez:
- `README.md` - Vue d'ensemble
- `GITHUB_SETUP.md` - Guide complet
- `CONFIGURATION.md` - Tous les paramètres
