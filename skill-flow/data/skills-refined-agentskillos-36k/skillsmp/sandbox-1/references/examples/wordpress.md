# WordPress + MySQL + phpMyAdmin

Complete LAMP stack deployment with WordPress and phpMyAdmin on separate ports.

## Result

| Service | Port | Public URL |
|---------|------|------------|
| WordPress | 80 | `https://wordpress-<sandbox>-<project>-<workspace>.us-1.buddy.app` |
| phpMyAdmin | 8080 | `https://phpmyadmin-<sandbox>-<project>-<workspace>.us-1.buddy.app` |

## Step 1: Create Sandbox with LAMP Stack

```bash
bdy sandbox create -i wordpress-lamp --resources 4x8 \
  --install-command "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 mariadb-server php php-mysql php-curl php-gd php-mbstring php-xml php-xmlrpc php-soap php-intl php-zip libapache2-mod-php unzip wget"
```

Wait for setup to complete:
```bash
bdy sandbox status wordpress-lamp
# Wait until Setup: SUCCESS
```

## Step 2: Configure MySQL

```bash
# Start MariaDB
bdy sandbox exec command wordpress-lamp "service mariadb start" --wait

# Create database and user
bdy sandbox exec command wordpress-lamp "mysql -e \"CREATE DATABASE wordpress; CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'wppass123'; GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost'; FLUSH PRIVILEGES;\"" --wait
```

## Step 3: Download WordPress and phpMyAdmin

```bash
# Download WordPress
bdy sandbox exec command wordpress-lamp "cd /var/www/html && wget -q https://wordpress.org/latest.tar.gz && tar -xzf latest.tar.gz && rm latest.tar.gz" --wait

# Download phpMyAdmin
bdy sandbox exec command wordpress-lamp "cd /var/www/html && wget -q https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.tar.gz && tar -xzf phpMyAdmin-5.2.1-all-languages.tar.gz && mv phpMyAdmin-5.2.1-all-languages phpmyadmin && rm phpMyAdmin-5.2.1-all-languages.tar.gz" --wait

# Set permissions
bdy sandbox exec command wordpress-lamp "chown -R www-data:www-data /var/www/html/wordpress /var/www/html/phpmyadmin" --wait
```

## Step 4: Configure WordPress

**Important:** Use write locally → cp pattern to avoid escaping issues.

```bash
# Create wp-config.php locally with proxy support
cat > /tmp/wp-config.php << 'EOF'
<?php
define('DB_NAME', 'wordpress');
define('DB_USER', 'wpuser');
define('DB_PASSWORD', 'wppass123');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

define('AUTH_KEY',         'unique-phrase-1');
define('SECURE_AUTH_KEY',  'unique-phrase-2');
define('LOGGED_IN_KEY',    'unique-phrase-3');
define('NONCE_KEY',        'unique-phrase-4');
define('AUTH_SALT',        'unique-phrase-5');
define('SECURE_AUTH_SALT', 'unique-phrase-6');
define('LOGGED_IN_SALT',   'unique-phrase-7');
define('NONCE_SALT',       'unique-phrase-8');

$table_prefix = 'wp_';
define('WP_DEBUG', false);

// CRITICAL: Proxy/HTTPS configuration for Buddy Sandbox
define('WP_HOME', 'https://wordpress-wordpress-lamp-<PROJECT>-<WORKSPACE>.us-1.buddy.app');
define('WP_SITEURL', 'https://wordpress-wordpress-lamp-<PROJECT>-<WORKSPACE>.us-1.buddy.app');
define('FORCE_SSL_ADMIN', true);
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}

if (!defined('ABSPATH')) {
    define('ABSPATH', __DIR__ . '/');
}
require_once ABSPATH . 'wp-settings.php';
EOF

# Copy to sandbox
bdy sandbox cp --silent /tmp/wp-config.php wordpress-lamp:/var/www/html/wordpress/wp-config.php
```

**Note:** Replace `<PROJECT>` and `<WORKSPACE>` with actual values, or get the URL after creating endpoints and update the config.

## Step 5: Configure phpMyAdmin

```bash
# Create config locally
cat > /tmp/phpmyadmin-config.php << 'EOF'
<?php
$cfg['blowfish_secret'] = 'abcdefghijklmnopqrstuvwxyz123456';
$i = 0;
$i++;
$cfg['Servers'][$i]['host'] = 'localhost';
$cfg['Servers'][$i]['compress'] = false;
$cfg['Servers'][$i]['AllowNoPassword'] = false;
EOF

# Copy to sandbox
bdy sandbox cp --silent /tmp/phpmyadmin-config.php wordpress-lamp:/var/www/html/phpmyadmin/config.inc.php
```

## Step 6: Configure Apache Virtual Hosts

```bash
# WordPress VirtualHost (port 80)
cat > /tmp/wordpress.conf << 'EOF'
<VirtualHost *:80>
    DocumentRoot /var/www/html/wordpress
    <Directory /var/www/html/wordpress>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF

# phpMyAdmin VirtualHost (port 8080)
cat > /tmp/phpmyadmin.conf << 'EOF'
Listen 8080
<VirtualHost *:8080>
    DocumentRoot /var/www/html/phpmyadmin
    <Directory /var/www/html/phpmyadmin>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF

# Copy configs
bdy sandbox cp --silent /tmp/wordpress.conf wordpress-lamp:/etc/apache2/sites-available/wordpress.conf
bdy sandbox cp --silent /tmp/phpmyadmin.conf wordpress-lamp:/etc/apache2/sites-available/phpmyadmin.conf

# Enable sites and start Apache
bdy sandbox exec command wordpress-lamp "a2dissite 000-default && a2ensite wordpress phpmyadmin && a2enmod rewrite && service apache2 start" --wait
```

## Step 7: Expose Endpoints

```bash
bdy sandbox endpoint add wordpress-lamp -n wordpress -e 80
bdy sandbox endpoint add wordpress-lamp -n phpmyadmin -e 8080
```

## Step 8: Verify

```bash
# Check Apache is listening on both ports
bdy sandbox exec command wordpress-lamp "ss -tlnp | grep apache" --wait

# Should show:
# *:80   ... apache2
# *:8080 ... apache2
```

## Credentials

| Service | Username | Password |
|---------|----------|----------|
| MySQL | wpuser | wppass123 |
| MySQL | root | (no password) |
| phpMyAdmin | wpuser | wppass123 |

## Troubleshooting

### WordPress redirects to localhost

**Symptom:** Opening WordPress URL redirects to `http://localhost/wp-admin/install.php`

**Cause:** WP_HOME and WP_SITEURL not set, or set after `require_once wp-settings.php`

**Fix:** Ensure wp-config.php has these lines BEFORE `require_once`:
```php
define('WP_HOME', 'https://your-public-url');
define('WP_SITEURL', 'https://your-public-url');
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}
```

### Apache not listening on port 8080

**Symptom:** phpMyAdmin endpoint returns connection refused

**Fix:** Restart Apache after adding the phpmyadmin.conf:
```bash
bdy sandbox exec command wordpress-lamp "service apache2 restart" --wait
```

### Services not running after sandbox restart

**Symptom:** After `bdy sandbox restart`, WordPress/phpMyAdmin don't work

**Fix:** Manually start services:
```bash
bdy sandbox exec command wordpress-lamp "service mariadb start && service apache2 start" --wait
```
