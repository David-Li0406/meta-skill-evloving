# 🚀 Automatisk Deployment till InfinityFree

Detta projekt är konfigurerat för automatisk deployment via GitHub Actions.

## 📋 Setup-instruktioner

### 1. Sätt upp GitHub Secrets

Gå till ditt GitHub repository:
```
Settings → Secrets and variables → Actions → New repository secret
```

Lägg till följande secrets:

| Secret Name | Value | Beskrivning |
|-------------|-------|-------------|
| `FTP_USERNAME` | `if0_40400950` | InfinityFree FTP username |
| `FTP_PASSWORD` | `qv19oAyv44J2xX` | InfinityFree FTP password |
| `ADMIN_PASSWORD` | `qv19oAyv44J2xX` | TheHUB admin lösenord |
| `DB_PASSWORD` | `qv19oAyv44J2xX` | MySQL databas lösenord |

### 2. Verifiera Workflow-konfiguration

Filen `.github/workflows/deploy.yml` innehåller:
- ✅ Automatisk trigger vid push till `main`/`master`
- ✅ Manuell trigger via GitHub Actions UI
- ✅ Skapar `.env` automatiskt med secrets
- ✅ FTP-upload till InfinityFree
- ✅ Exkluderar onödiga filer (.git, backups, etc.)

### 3. Hur det fungerar

1. **Gör ändringar lokalt** (t.ex. via Claude Code)
2. **Commit och push till GitHub:**
   ```bash
   git add .
   git commit -m "Din commit-message"
   git push origin main
   ```
3. **GitHub Action startar automatiskt** 🎯
4. **Deploy sker till InfinityFree** ⚡
5. **Klart! Site uppdaterat** ✅

### 4. Manuell deploy

Du kan också köra deployment manuellt:
1. Gå till **Actions** i GitHub
2. Välj **Deploy to InfinityFree**
3. Klicka **Run workflow**
4. Välj branch och klicka **Run workflow**

### 5. Övervaka deployment

Gå till **Actions** i GitHub för att:
- ✅ Se deployment-status (körs, lyckades, misslyckades)
- 📋 Läsa loggar från deployment
- 🔄 Re-run misslyckade deployments

## 🔒 Säkerhetsnotering

- `.env`-filen skapas automatiskt under deployment från GitHub Secrets
- Känsliga credentials finns ALDRIG i git history
- FTP-credentials är säkrade via GitHub Secrets

## 🎯 FTP-Destination

- **Server:** ftpupload.net
- **Directory:** /htdocs/
- **Protocol:** FTP

## 📝 Exkluderade filer

Följande filer/mappar uploaderas INTE till produktionsservern:
- `.git` och alla git-filer
- `node_modules/`
- `vendor/`
- `*.backup` filer
- `backup/` mapp
- Dokumentation (AUDIT_REPORT.md, SECURITY.md, README.md)

## ✅ Checklist för första deployment

- [ ] Secrets konfigurerade i GitHub
- [ ] Workflow-filen committad till repository
- [ ] Databas-schema körd på InfinityFree MySQL
- [ ] FTP-credentials verifierade
- [ ] Push till main branch
- [ ] Övervaka deployment i Actions

## 🆘 Felsökning

**Problem:** Deployment misslyckas med "Authentication failed"
- **Lösning:** Verifiera FTP_USERNAME och FTP_PASSWORD i GitHub Secrets

**Problem:** .env-filen saknas på servern
- **Lösning:** Kontrollera att alla secrets (ADMIN_PASSWORD, DB_PASSWORD) är konfigurerade

**Problem:** Filer uploaderas inte
- **Lösning:** Kontrollera `server-dir` i deploy.yml (ska vara `/htdocs/`)

## 📞 Support

InfinityFree support: https://forum.infinityfree.com/
GitHub Actions docs: https://docs.github.com/actions
