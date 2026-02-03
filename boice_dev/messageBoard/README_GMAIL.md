# Using Gmail SMTP for Password Reset (Production)

This document explains how to configure your existing Gmail account to send password-reset emails from the app in production.

---

## 1) Recommended account type
- For a production app, prefer **Google Workspace (G Suite)** for better deliverability and domain control. Consumer Gmail accounts work but have stricter daily sending limits and fewer domain configuration options.

## 2) Security: enable 2-Step Verification and create an App Password
1. Sign in to your Google account at https://myaccount.google.com
2. Go to **Security** → **2-Step Verification** and enable it if it isn't already.
3. In **Security** → **App passwords**, create a new app password:
   - Select **Mail** and the device (or choose "Other" and name it e.g. `PDXTricking SMTP`).
   - Google will show a 16-character app password — copy it now (this is your SMTP password).

> Note: Google removed the "Allow less secure apps" option; use **App Passwords** when 2FA is enabled.

## 3) Set environment variables (example `.env` entries)
Add these to your environment (or to your `.env`, but DO NOT commit secrets):

```
SECRET_KEY=replace-with-a-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your_16_char_app_password
MAIL_DEFAULT_SENDER='Your App <noreply@yourdomain.com>'
```

- `MAIL_USERNAME` is your Gmail address.
- `MAIL_PASSWORD` is the App Password generated above.
- `MAIL_DEFAULT_SENDER` should be an address you control — set a friendly sender name.

### Raspberry Pi — Apache2 (shell commands only)

```bash
# Option 1: append env vars to Apache's envvars (applies to all Apache child processes)
sudo tee -a /etc/apache2/envvars > /dev/null <<'EOF'
export SECRET_KEY='replace-with-a-secret'
export MAIL_SERVER='smtp.gmail.com'
export MAIL_PORT='587'
export MAIL_USE_TLS='True'
export MAIL_USE_SSL='False'
export MAIL_USERNAME='your.email@gmail.com'
export MAIL_PASSWORD='your_app_password'
export MAIL_DEFAULT_SENDER='Your App <noreply@yourdomain.com>'
EOF

# Secure the file (optional)
sudo chown root:root /etc/apache2/envvars && sudo chmod 640 /etc/apache2/envvars

# Restart Apache to apply changes
sudo systemctl restart apache2


# Option 2: add SetEnv entries to your Apache site conf (e.g., /etc/apache2/sites-available/pdxtricking.conf)
sudo tee /etc/apache2/sites-available/pdxtricking.conf > /dev/null <<'EOF'
<VirtualHost *:80>
    ServerName example.com

    WSGIDaemonProcess pdxtricking python-home=/home/pi/venv python-path=/home/pi/PDXTricking/boice_dev/messageBoard
    WSGIScriptAlias / /home/pi/PDXTricking/boice_dev/messageBoard/pdxtricking.wsgi

    <Directory /home/pi/PDXTricking/boice_dev/messageBoard>
        Require all granted
    </Directory>

    SetEnv SECRET_KEY 'replace-with-a-secret'
    SetEnv MAIL_SERVER 'smtp.gmail.com'
    SetEnv MAIL_PORT '587'
    SetEnv MAIL_USE_TLS 'True'
    SetEnv MAIL_USE_SSL 'False'
    SetEnv MAIL_USERNAME 'your.email@gmail.com'
    SetEnv MAIL_PASSWORD 'your_app_password'
    SetEnv MAIL_DEFAULT_SENDER 'Your App <noreply@yourdomain.com>'
</VirtualHost>
EOF

# Enable the site and reload Apache
sudo a2ensite pdxtricking
sudo systemctl reload apache2


# Option 3: use a .env in the app directory (dev only). Create the file and secure it:
cd /home/pi/PDXTricking/boice_dev/messageBoard
sudo tee .env > /dev/null <<'EOF'
SECRET_KEY=replace-with-a-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER='Your App <noreply@yourdomain.com>'
EOF
sudo chown pi:pi .env
sudo chmod 600 .env

# After changing Apache config or envvars, always reload Apache:
sudo systemctl reload apache2
```

## 4) App configuration reminders

## 4) App configuration reminders
- Our `app.py` expects the above env vars (see `.env.example`).
- Ensure your production web server runs under HTTPS (TLS) — do not expose password-reset links over plain HTTP.
- Tokens are time-limited (1 hour by default) — this is already implemented.

## 5) Testing in production-like environment
1. Deploy app to a staging server reachable over HTTPS.
2. Set the env vars on the server (systemd service file, hosting dashboard secrets, or a secrets manager).
3. Trigger a password-reset from the UI and check the recipient inbox.
4. Check app logs for any SMTP errors if mail doesn’t arrive.

## 6) Delivery limits and reliability
- Consumer Gmail accounts have low daily limits (do not rely on them for sending tens/hundreds of transactional emails). Consider Google Workspace or a transactional provider (SendGrid, Mailgun, Amazon SES) for heavier use.
- For custom domains and better deliverability, verify the sending domain and configure SPF/DKIM if you switch to a provider or use Workspace.

## 7) Production best practices
- Store credentials securely (environment variables, secrets manager). Do not commit `.env` files.
- Rotate app passwords occasionally and revoke if compromised.
- Send email asynchronously (the app uses a background thread; consider Celery or RQ for scale).
- Add rate limiting to password-reset requests and monitor logs for abuse.

---

If you want, I can:
- Add a short `/docs` section showing how to set the env vars on Windows/PowerShell or Linux systemd, or
- Replace Gmail with SendGrid/Mailgun integration and add billing-friendly configuration for production.

Which would you like next? ✅