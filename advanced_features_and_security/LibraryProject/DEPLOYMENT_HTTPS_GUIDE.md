# HTTPS Deployment Guide - LibraryProject

## Overview
This guide provides comprehensive instructions for deploying the LibraryProject Django application with HTTPS support, including SSL/TLS certificate setup, web server configuration, and security best practices.

## Prerequisites
- SSL/TLS certificate (Let's Encrypt recommended)
- Web server (Nginx or Apache)
- Domain name configured to point to your server
- Access to server terminal with sudo privileges

## Step 1: SSL Certificate Setup

### Using Let's Encrypt (Recommended)
```bash
# Install Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx  # For Nginx
# OR
sudo apt install certbot python3-certbot-apache  # For Apache

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
# OR
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
```

### Manual Certificate Installation
```bash
# Create certificate directory
sudo mkdir -p /etc/ssl/certs/
sudo mkdir -p /etc/ssl/private/

# Copy certificate files
sudo cp your_certificate.crt /etc/ssl/certs/
sudo cp your_private.key /etc/ssl/private/
sudo cp intermediate_certificate.crt /etc/ssl/certs/
```

## Step 2: Web Server Configuration

### Nginx Configuration
Create `/etc/nginx/sites-available/libraryproject`:

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'none';" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Static files
    location /static/ {
        alias /path/to/your/project/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Apache Configuration
Create `/etc/apache2/sites-available/libraryproject.conf`:

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    # SSL security settings
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off
    SSLSessionTickets off
    
    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # Content Security Policy
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'none';"
    
    # Static files
    Alias /static /path/to/your/project/static
    <Directory /path/to/your/project/static>
        Require all granted
    </Directory>
    
    # Media files
    Alias /media /path/to/your/project/media
    <Directory /path/to/your/project/media>
        Require all granted
    </Directory>
    
    # WSGI configuration
    WSGIDaemonProcess libraryproject python-path=/path/to/your/project
    WSGIProcessGroup libraryproject
    WSGIScriptAlias / /path/to/your/project/LibraryProject/wsgi.py
    
    <Directory /path/to/your/project/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

## Step 3: Django Production Settings

### Environment Variables Setup
Create `.env` file in your project root:

```bash
# Security settings
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database settings (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/libraryproject

# Email settings (for password reset, etc.)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Production Settings Configuration
Update `settings.py` for production:

```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'

# Database (PostgreSQL recommended)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'libraryproject'),
        'USER': os.environ.get('DB_USER', 'libraryuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## Step 4: SSL Certificate Auto-Renewal

### Let's Encrypt Auto-Renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Add to crontab for automatic renewal
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

## Step 5: Security Testing

### SSL Labs Test
1. Visit https://www.ssllabs.com/ssltest/
2. Enter your domain name
3. Verify A+ rating

### Security Headers Test
1. Visit https://securityheaders.com/
2. Enter your domain name
3. Verify all security headers are properly configured

### Manual Testing
```bash
# Test HTTPS redirect
curl -I http://yourdomain.com

# Test security headers
curl -I https://yourdomain.com

# Test HSTS
curl -I -H "User-Agent: Mozilla/5.0" https://yourdomain.com
```

## Step 6: Deployment Checklist

### Pre-deployment
- [ ] SSL certificate obtained and configured
- [ ] Web server configured with HTTPS
- [ ] Django settings updated for production
- [ ] Environment variables configured
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Database migrations applied: `python manage.py migrate`
- [ ] Superuser created: `python manage.py createsuperuser`

### Post-deployment
- [ ] Test HTTPS redirect
- [ ] Verify SSL certificate validity
- [ ] Test all application functionality
- [ ] Verify security headers
- [ ] Test form submissions
- [ ] Check admin interface access
- [ ] Verify file uploads work correctly

## Step 7: Monitoring and Maintenance

### SSL Certificate Monitoring
```bash
# Check certificate expiry
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/cert.pem -text -noout | grep "Not After"

# Set up monitoring alerts
# Use services like UptimeRobot or Pingdom
```

### Security Updates
```bash
# Regular security updates
sudo apt update && sudo apt upgrade

# Update Django and dependencies
pip install --upgrade django
pip install --upgrade -r requirements.txt
```

## Troubleshooting

### Common Issues

1. **Mixed Content Warnings**
   - Ensure all resources (CSS, JS, images) use HTTPS
   - Update any hardcoded HTTP URLs

2. **Certificate Errors**
   - Verify certificate chain is complete
   - Check certificate expiry dates
   - Ensure domain matches certificate

3. **HSTS Issues**
   - Clear browser cache if testing with HSTS
   - Use incognito/private mode for testing

4. **CSRF Token Issues**
   - Ensure CSRF_COOKIE_SECURE matches your environment
   - Check that HTTPS is properly configured

## Support and Resources

- Let's Encrypt Documentation: https://letsencrypt.org/docs/
- Django Security Documentation: https://docs.djangoproject.com/en/stable/topics/security/
- Mozilla SSL Configuration Generator: https://ssl-config.mozilla.org/
- SSL Labs Best Practices: https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices

## Contact
For deployment support or security questions, contact the development team.
