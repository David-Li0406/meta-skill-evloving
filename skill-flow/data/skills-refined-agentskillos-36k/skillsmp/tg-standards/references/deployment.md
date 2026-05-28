# Deployment Patterns

## Required Environment Variables

```bash
DJANGO_ENVIRONMENT=production
SECRET_KEY=<generated-secret-key>
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com
DB_NAME=tg_db
DB_USER=tg_user
DB_PASSWORD=<secure-password>
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://127.0.0.1:6379/1
```

## Security Settings (Production)

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
```

Verify: `python manage.py check --deploy`

## Deployment Steps

```bash
# 1. Backup database
pg_dump production_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Enable maintenance mode
touch /var/www/tg/maintenance.flag

# 3. Pull code
git fetch origin && git checkout <branch> && git pull

# 4. Install dependencies
pip install -r requirements.txt --upgrade

# 5. Validate data
python manage.py validate_data_integrity --verbose

# 6. Run migrations
python manage.py showmigrations
python manage.py migrate

# 7. Collect static
python manage.py collectstatic --noinput

# 8. Restart services
sudo systemctl restart gunicorn nginx

# 9. Disable maintenance mode
rm /var/www/tg/maintenance.flag

# 10. Health check
curl -I https://your-domain.com/
python manage.py monitor_validation
```

## Rollback

### Code-only
```bash
git log --oneline
git checkout <previous-commit>
sudo systemctl restart gunicorn
```

### Full Rollback
```bash
sudo systemctl stop gunicorn
pg_restore -d production_db backup_TIMESTAMP.sql
git checkout <previous-commit>
python manage.py migrate <app> <previous-migration>
sudo systemctl start gunicorn
```

## Checklist

- [ ] All tests passing
- [ ] Database backup created
- [ ] Rollback plan documented
- [ ] Data validation passed
- [ ] Migrations applied
- [ ] Health check passed
- [ ] Monitor for 30 minutes
