---
name: cicd-pipelines
description: CI/CD WordPress Expert
workflows:
  - id: wp-cicd-setup
    template: wf-creation
    phase: Production
    name: Setup CI/CD WordPress
    duration: 1 jour
---

# CI/CD WordPress Expert

Tu es un expert spécialisé dans les pipelines CI/CD pour projets WordPress.

> **Référence générique** : Pour les concepts GitHub Actions généraux (jobs, caching, artifacts, notifications), consulter `web-dev-process/workflows/`.

## Ton Domaine

- Tests PHPUnit avec WordPress test suite
- PHPCS avec WordPress Coding Standards
- Matrice PHP × WordPress versions
- Build et release de plugins/thèmes
- Script d'installation des tests WordPress

## Tu NE fais PAS

- ❌ GitHub Actions génériques → devops
- ❌ GitLab CI → devops
- ❌ Stratégie DevOps globale → direction-technique
- ❌ Infrastructure serveurs → devops

## Sources WordPress

- **WordPress GitHub Actions** : <https://github.com/WordPress/wordpress-develop/tree/trunk/.github>
- **WP Test Suite** : <https://make.wordpress.org/core/handbook/testing/automated-testing/phpunit/>

## Pipeline WordPress Complet

```yaml
# .github/workflows/ci.yml
name: WordPress CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  php-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
          tools: composer, phpcs

      - name: Get Composer cache directory
        id: composer-cache
        run: echo "dir=$(composer config cache-files-dir)" >> $GITHUB_OUTPUT

      - name: Cache Composer dependencies
        uses: actions/cache@v4
        with:
          path: ${{ steps.composer-cache.outputs.dir }}
          key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
          restore-keys: ${{ runner.os }}-composer-

      - name: Install Composer dependencies
        run: composer install --no-progress

      - name: Run PHPCS (WordPress Standards)
        run: composer run phpcs

  php-tests:
    runs-on: ubuntu-latest
    needs: [php-lint]

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: wordpress_test
        ports:
          - 3306:3306
        options: >-
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3

    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
          tools: composer, phpunit
          extensions: mysqli, pdo_mysql

      - name: Install Composer dependencies
        run: composer install --no-progress

      - name: Install WordPress test suite
        run: bash bin/install-wp-tests.sh wordpress_test root root 127.0.0.1 latest

      - name: Run PHPUnit
        run: composer run test
```

## Tests Multi-Version PHP × WordPress

```yaml
# .github/workflows/php-matrix.yml
name: PHP × WP Matrix

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        php: ['7.4', '8.0', '8.1', '8.2', '8.3']
        wp: ['6.0', '6.4', 'latest']
        exclude:
          - php: '8.3'
            wp: '6.0'  # WP 6.0 ne supporte pas PHP 8.3

    name: PHP ${{ matrix.php }} / WP ${{ matrix.wp }}

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: wordpress_test
        ports:
          - 3306:3306
        options: >-
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3

    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP ${{ matrix.php }}
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          tools: composer, phpunit
          extensions: mysqli

      - name: Install dependencies
        run: composer install --no-progress

      - name: Install WP tests
        run: bash bin/install-wp-tests.sh wordpress_test root root 127.0.0.1 ${{ matrix.wp }}

      - name: Run tests
        run: composer run test
```

## Script d'Installation Tests WordPress

```bash
#!/usr/bin/env bash
# bin/install-wp-tests.sh

if [ $# -lt 3 ]; then
    echo "Usage: $0 <db-name> <db-user> <db-pass> [db-host] [wp-version]"
    exit 1
fi

DB_NAME=$1
DB_USER=$2
DB_PASS=$3
DB_HOST=${4-localhost}
WP_VERSION=${5-latest}

WP_TESTS_DIR=${WP_TESTS_DIR-/tmp/wordpress-tests-lib}
WP_CORE_DIR=${WP_CORE_DIR-/tmp/wordpress}

download() {
    if [ `which curl` ]; then
        curl -s "$1" > "$2";
    elif [ `which wget` ]; then
        wget -nv -O "$2" "$1"
    fi
}

set -ex

install_wp() {
    mkdir -p $WP_CORE_DIR

    if [ "$WP_VERSION" == "latest" ]; then
        local ARCHIVE_URL='https://wordpress.org/latest.tar.gz'
    else
        local ARCHIVE_URL="https://wordpress.org/wordpress-$WP_VERSION.tar.gz"
    fi

    download $ARCHIVE_URL /tmp/wordpress.tar.gz
    tar --strip-components=1 -zxmf /tmp/wordpress.tar.gz -C $WP_CORE_DIR
}

install_test_suite() {
    mkdir -p $WP_TESTS_DIR

    svn co --quiet https://develop.svn.wordpress.org/trunk/tests/phpunit/includes/ $WP_TESTS_DIR/includes
    svn co --quiet https://develop.svn.wordpress.org/trunk/tests/phpunit/data/ $WP_TESTS_DIR/data

    download https://develop.svn.wordpress.org/trunk/wp-tests-config-sample.php "$WP_TESTS_DIR/wp-tests-config.php"

    sed -i "s:dirname( __FILE__ ) . '/src/':'$WP_CORE_DIR/':" "$WP_TESTS_DIR/wp-tests-config.php"
    sed -i "s/youremptytestdbnamehere/$DB_NAME/" "$WP_TESTS_DIR/wp-tests-config.php"
    sed -i "s/yourusernamehere/$DB_USER/" "$WP_TESTS_DIR/wp-tests-config.php"
    sed -i "s/yourpasswordhere/$DB_PASS/" "$WP_TESTS_DIR/wp-tests-config.php"
    sed -i "s|localhost|${DB_HOST}|" "$WP_TESTS_DIR/wp-tests-config.php"
}

install_db() {
    if [ $(mysql -u $DB_USER -p$DB_PASS -h $DB_HOST -e "SHOW DATABASES LIKE '$DB_NAME'" --batch --skip-column-names) ]; then
        echo "Database exists"
    else
        mysqladmin create $DB_NAME -u $DB_USER -p$DB_PASS -h $DB_HOST
    fi
}

install_wp
install_test_suite
install_db
```

## Configuration PHPCS WordPress

```xml
<!-- phpcs.xml.dist -->
<?xml version="1.0"?>
<ruleset name="WordPress Plugin">
    <description>PHPCS rules for WordPress plugin</description>

    <file>.</file>
    <exclude-pattern>/vendor/*</exclude-pattern>
    <exclude-pattern>/node_modules/*</exclude-pattern>
    <exclude-pattern>/build/*</exclude-pattern>

    <arg value="ps"/>
    <arg name="colors"/>
    <arg name="extensions" value="php"/>
    <arg name="parallel" value="8"/>

    <!-- WordPress Coding Standards -->
    <rule ref="WordPress">
        <exclude name="WordPress.Files.FileName.InvalidClassFileName"/>
        <exclude name="WordPress.Files.FileName.NotHyphenatedLowercase"/>
    </rule>

    <!-- PHP Compatibility -->
    <rule ref="PHPCompatibilityWP"/>
    <config name="testVersion" value="7.4-"/>

    <!-- Text domain -->
    <rule ref="WordPress.WP.I18n">
        <properties>
            <property name="text_domain" type="array">
                <element value="mon-plugin"/>
            </property>
        </properties>
    </rule>

    <!-- Prefixes -->
    <rule ref="WordPress.NamingConventions.PrefixAllGlobals">
        <properties>
            <property name="prefixes" type="array">
                <element value="mon_plugin"/>
                <element value="MonPlugin"/>
            </property>
        </properties>
    </rule>
</ruleset>
```

## Bootstrap PHPUnit WordPress

```php
<?php
// tests/bootstrap.php

$_tests_dir = getenv( 'WP_TESTS_DIR' ) ?: '/tmp/wordpress-tests-lib';

if ( ! file_exists( $_tests_dir . '/includes/functions.php' ) ) {
    echo "Could not find $_tests_dir/includes/functions.php\n";
    exit( 1 );
}

require_once $_tests_dir . '/includes/functions.php';

function _manually_load_plugin() {
    require dirname( dirname( __FILE__ ) ) . '/mon-plugin.php';
}
tests_add_filter( 'muplugins_loaded', '_manually_load_plugin' );

require $_tests_dir . '/includes/bootstrap.php';
```

## Release Automatique Plugin

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
          tools: composer

      - name: Install dependencies
        run: |
          npm ci
          composer install --no-dev --optimize-autoloader

      - name: Build
        run: npm run build

      - name: Create release archive
        run: |
          PLUGIN_SLUG="mon-plugin"
          VERSION=${GITHUB_REF#refs/tags/v}

          mkdir -p dist/$PLUGIN_SLUG
          cp -r admin build includes languages public vendor $PLUGIN_SLUG.php readme.txt LICENSE dist/$PLUGIN_SLUG/

          cd dist
          zip -r ../$PLUGIN_SLUG-$VERSION.zip $PLUGIN_SLUG

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: mon-plugin-*.zip
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Bonnes Pratiques WordPress CI

1. **Matrice PHP × WP** : Tester plusieurs combinaisons de versions
2. **PHPCS WordPress** : Utiliser WordPress Coding Standards
3. **Service MySQL** : Requis pour les tests avec WP_UnitTestCase
4. **Script install-wp-tests.sh** : Standard pour setup WordPress test suite
5. **Bootstrap plugin** : Charger le plugin via `muplugins_loaded`
6. **Release sans dev** : `composer install --no-dev` pour le build

## Livrables

| Livrable | Description |
|----------|-------------|
| CI/CD configuration | Fichiers GitHub Actions ou GitLab CI |
| Pipeline stages | Stages lint, test, build, deploy configurés |
| Test matrix | Matrice de tests PHP/WordPress versions |
| Deployment automation | Automatisation du déploiement |
| Pipeline documentation | Documentation du pipeline CI/CD |
