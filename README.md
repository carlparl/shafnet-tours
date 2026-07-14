# Shafnet Tours & Travel Ltd

A Django website for presenting Uganda tours, safari itineraries, destinations and travel enquiries.

## Main features

- Responsive public website with a forest-green visual system
- Domestic getaway and international safari filters
- Tour details, day-by-day itineraries and booking enquiries
- Destination, testimonial and gallery management through Django admin
- Contact and booking email notifications
- Accessible navigation, labelled forms and mobile-friendly layouts

## Local setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Create a `.env` file for local settings. At minimum:

```env
SECRET_KEY=replace-with-a-strong-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Production settings

Set these environment variables on the hosting service:

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=your-domain.example`
- `CSRF_TRUSTED_ORIGINS=https://your-domain.example`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `BOOKING_NOTIFICATION_EMAIL=info@shafnettours.com`

For SMTP email delivery, also set `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` and `DEFAULT_FROM_EMAIL`.

Before deployment, run:

```bash
python manage.py check --deploy
python manage.py test
python manage.py collectstatic --noinput
```
