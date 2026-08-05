# Configuration des Secrets GitHub - Dynatrace Daily Health

## 1. Accéder aux paramètres du repository

1. Allez sur: https://github.com/marcdubrulle-arch/dynatrace-daily-health/settings/secrets/actions
2. Vous êtes maintenant dans **Settings → Secrets and variables → Actions**

## 2. Ajouter les Secrets Dynatrace

### DYNATRACE_BASE_URL
1. Cliquez sur "New repository secret"
2. **Name:** `DYNATRACE_BASE_URL`
3. **Value:** `https://uxw82338.live.dynatrace.com`
4. Cliquez "Add secret"

### DYNATRACE_API_TOKEN
1. Cliquez sur "New repository secret"
2. **Name:** `DYNATRACE_API_TOKEN`
3. **Value:** Votre token Dynatrace (ex: `dt0c01.R6JVKET3QH25PQ2KXVIFQUGE.FTB5R...`)
   - ⚠️ Assurez-vous que le token a les scopes:
     - `entities.read` (lecture des entités)
     - `metrics.read` (lecture des métriques)
     - `problems.read` (lecture des problèmes)
4. Cliquez "Add secret"

## 3. Configurer l'Email (Recommandé)

Si vous avez un serveur SMTP (ex: Gmail, Orange, etc):

### Pour Gmail:
```
SMTP_SERVER: smtp.gmail.com
SMTP_PORT: 587
SMTP_USER: votre.email@gmail.com
SMTP_PASSWORD: Votre mot de passe d'app Gmail
EMAIL_FROM: votre.email@gmail.com
EMAIL_TO: marc.dubrulle@orange.com
```

### Pour Orange Mail:
```
SMTP_SERVER: smtp.wanadoo.fr
SMTP_PORT: 587
SMTP_USER: votre.email@orange.fr
SMTP_PASSWORD: Votre mot de passe Orange
EMAIL_FROM: votre.email@orange.fr
EMAIL_TO: marc.dubrulle@orange.com
```

### Pour Outlook/Hotmail:
```
SMTP_SERVER: smtp-mail.outlook.com
SMTP_PORT: 587
SMTP_USER: votre.email@outlook.com
SMTP_PASSWORD: Votre mot de passe Outlook
EMAIL_FROM: votre.email@outlook.com
EMAIL_TO: marc.dubrulle@orange.com
```

## 4. Ajouter les Secrets Email à GitHub

Répétez l'étape "New repository secret" pour chacun:

1. **SMTP_SERVER** = `smtp.xyz.com`
2. **SMTP_PORT** = `587`
3. **SMTP_USER** = `votre.utilisateur@domain.com`
4. **SMTP_PASSWORD** = `votre mot de passe`
5. **EMAIL_FROM** = `votre.email@domain.com`
6. **EMAIL_TO** = `marc.dubrulle@orange.com` (ou plusieurs: `email1@xyz.com,email2@xyz.com`)

## 5. Tester le Workflow

1. Allez sur: https://github.com/marcdubrulle-arch/dynatrace-daily-health/actions
2. Sélectionnez le workflow **"Daily Dynatrace Health"**
3. Cliquez sur **"Run workflow"** → **"Run workflow"**
4. Attendez quelques minutes que le workflow s'exécute
5. Vérifiez les logs et les artefacts générés

## 6. Vérifier les Résultats

Après le test:
- ✓ Un rapport Markdown sera généré en artefact
- ✓ Un rapport JSON sera disponible
- ✓ Si l'email est configuré, vous recevrez un email HTML formaté

## Notes de Sécurité

- ⚠️ Ne commitez **jamais** les tokens ou mots de passe dans le code
- ✓ Les secrets GitHub sont chiffrés et masqués dans les logs
- ✓ Chaque workflow run a accès aux secrets via les variables d'environnement

## Créer un Token Dynatrace

Si vous n'avez pas encore de token:

1. Allez dans Dynatrace: **Settings → Integration → Dynatrace API**
2. Cliquez **"Create token"**
3. Configurez:
   - **Token name:** "Daily Health Check"
   - **Scopes:** Sélectionnez:
     - `entities.read`
     - `metrics.read`
     - `problems.read`
4. Cliquez **"Generate"**
5. Copiez le token et collez-le dans le secret `DYNATRACE_API_TOKEN` GitHub

---

Une fois configuré, le workflow tournera automatiquement chaque jour à **18:00 UTC** (20:00 CEST) et vous recevrez le rapport par email!
