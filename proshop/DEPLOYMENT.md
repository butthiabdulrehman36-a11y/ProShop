# ProShop Deployment Guide

## Production Checklist

Before deploying ProShop to a live HTTPS server:

1. Set `DJANGO_DEBUG=False`
2. Set `DJANGO_ALLOWED_HOSTS` to the production domain
3. Set `DJANGO_SECURE_SSL_REDIRECT=True`
4. Set `DJANGO_SESSION_COOKIE_SECURE=True`
5. Set `DJANGO_CSRF_COOKIE_SECURE=True`
6. Configure `DJANGO_SECURE_HSTS_SECONDS` only after HTTPS is working correctly
7. Keep `DJANGO_SECRET_KEY` private
8. Run `python manage.py check --deploy`
9. Run `python manage.py collectstatic --noinput`
10. Create a fresh database backup before deployment

## Current Local Development

The current local development configuration uses:

- `DEBUG=True`
- `127.0.0.1`
- `localhost`
- HTTP development mode

These values must be changed through `.env` before production deployment.

## Important Security Notes

- Never commit `.env` to Git.
- Never publish the Django `SECRET_KEY`.
- Production must use HTTPS.
- Production should use a production-ready database configuration.
- Review all deployment settings before making the site publicly accessible.