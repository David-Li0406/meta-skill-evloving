# Deployment Reference

## Table of Contents
1. [OpenShift Operator Deployment](#openshift-operator-deployment)
2. [Docker Compose Development](#docker-compose-development)
3. [Custom Image Building](#custom-image-building)
4. [Environment Variables](#environment-variables)
5. [TLS/SSL Configuration](#tlsssl-configuration)

## OpenShift Operator Deployment

### Red Hat Keycloak Operator (v2alpha1)

The Red Hat Keycloak Operator manages Keycloak instances on OpenShift/Kubernetes using the `k8s.keycloak.org/v2alpha1` API.

### Complete Keycloak CR Example

```yaml
apiVersion: k8s.keycloak.org/v2alpha1
kind: Keycloak
metadata:
  name: keycloak
  labels:
    app: keycloak
  namespace: my-keycloak-namespace
spec:
  # Database configuration
  db:
    vendor: mysql  # mysql, postgres, mariadb
    host: mysql.database.svc.cluster.local
    port: 6446
    database: keycloak_prod
    usernameSecret:
      name: mysql-db-keycloak-secret
      key: username
    passwordSecret:
      name: mysql-db-keycloak-secret
      key: password

  # HTTP configuration
  http:
    httpEnabled: true
    httpPort: 8080
    httpsPort: 8443
    tlsSecret: keycloak-tls

  # Proxy headers (required behind ingress/route)
  proxy:
    headers: xforwarded

  # Hostname configuration
  hostname:
    hostname: https://keycloak.example.com
    admin: https://admin-keycloak.example.com
    strict: false  # Allow multiple hostnames

  # Number of replicas
  instances: 2

  # Custom image with providers
  image: quay.io/my-org/keycloak:custom-tag
  imagePullSecrets:
    - name: registry-pull-secret

  # Use optimized startup (production)
  startOptimized: true

  # Custom environment variables via podTemplate
  unsupported:
    podTemplate:
      spec:
        containers:
          - name: keycloak
            env:
              # Custom database for providers
              - name: FLEXII_DB_URL
                valueFrom:
                  secretKeyRef:
                    name: flexii-keycloak-db-secret
                    key: url
              - name: FLEXII_DB_USER
                valueFrom:
                  secretKeyRef:
                    name: flexii-keycloak-db-secret
                    key: username
              - name: FLEXII_DB_PASSWORD
                valueFrom:
                  secretKeyRef:
                    name: flexii-keycloak-db-secret
                    key: password
              # Feature flags
              - name: ENABLE_DB_INITIALIZATION
                value: "true"
            # Resource limits
            resources:
              limits:
                memory: 2Gi
                cpu: 1000m
              requests:
                memory: 1Gi
                cpu: 500m
```

### Required Secrets

**Database Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-db-keycloak-secret
  namespace: my-keycloak-namespace
type: Opaque
stringData:
  username: keycloak
  password: secure-password
```

**TLS Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: keycloak-tls
  namespace: my-keycloak-namespace
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-certificate>
  tls.key: <base64-encoded-private-key>
```

**Image Pull Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: registry-pull-secret
  namespace: my-keycloak-namespace
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
```

### OpenShift Route

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: keycloak
  namespace: my-keycloak-namespace
spec:
  host: keycloak.example.com
  to:
    kind: Service
    name: keycloak-service
  port:
    targetPort: https
  tls:
    termination: reencrypt
    insecureEdgeTerminationPolicy: Redirect
```

### Key Configuration Points

| Setting | Production Value | Description |
|---------|-----------------|-------------|
| `instances` | ≥2 | High availability |
| `startOptimized` | true | Pre-built optimized image |
| `proxy.headers` | xforwarded | Trust proxy headers |
| `hostname.strict` | false | Multiple hostnames allowed |
| `http.httpEnabled` | true | Required for health checks |

## Docker Compose Development

### Complete Development Stack

```yaml
# Note: 'version' is obsolete in Docker Compose v2+ and can be omitted
services:
  mysql:
    image: mysql:8.3.0
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: keycloak
      MYSQL_USER: keycloak
      MYSQL_PASSWORD: password
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - keycloak-network
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 10

  flexii-oracle:
    image: gvenzl/oracle-xe:21
    restart: unless-stopped
    environment:
      ORACLE_PASSWORD: oracle123
      APP_USER: flexii_user
      APP_USER_PASSWORD: flexii_password
    volumes:
      - flexii_oracle_data:/opt/oracle/oradata
      - ./scripts/init-flexii-db.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - keycloak-network
    ports:
      - "1521:1521"
    healthcheck:
      test: ["CMD", "sh", "-c", "sqlplus -L flexii_user/flexii_password@//localhost:1521/XE @/dev/null <<< 'SELECT 1 FROM DUAL;'"]
      interval: 30s
      timeout: 10s
      retries: 10
      start_period: 300s

  keycloak:
    build:
      context: .
      dockerfile: Dockerfile
    restart: unless-stopped
    depends_on:
      mysql:
        condition: service_healthy
      flexii-oracle:
        condition: service_healthy
    command: ["start-dev"]
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin123
      KC_DB: mysql
      KC_DB_URL: jdbc:mysql://mysql:3306/keycloak?characterEncoding=UTF-8
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: password
      # Custom provider databases
      FLEXII_DB_URL: jdbc:oracle:thin:@flexii-oracle:1521:XE
      FLEXII_DB_USER: flexii_user
      FLEXII_DB_PASSWORD: flexii_password
      ENABLE_DB_INITIALIZATION: "true"
    networks:
      - keycloak-network
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8080/health/ready || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 15
      start_period: 180s

  keycloak-config:
    build:
      context: .
      dockerfile: Dockerfile.config
    depends_on:
      keycloak:
        condition: service_healthy
    environment:
      KEYCLOAK_CONFIG_SERVER_URI: http://keycloak:8080
      KEYCLOAK_HEALTH_URL: http://keycloak:8080/health/ready
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin123
      AZURE_CLIENT_ID: ${AZURE_CLIENT_ID}
      AZURE_CLIENT_SECRET: ${AZURE_CLIENT_SECRET}
      AZURE_TENANT_ID: ${AZURE_TENANT_ID}
    networks:
      - keycloak-network

networks:
  keycloak-network:
    driver: bridge

volumes:
  mysql_data:
  flexii_oracle_data:
```

### Commands

```bash
# Start all services
docker compose up -d

# Start with rebuild
docker compose up --build -d

# View logs
docker compose logs -f keycloak

# Stop and clean
docker compose down -v
```

## Custom Image Building

### Dockerfile for Keycloak with Providers

```dockerfile
FROM quay.io/keycloak/keycloak:26.3.1 AS builder

# Enable health and metrics support
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Configure database vendor
ENV KC_DB=mysql

WORKDIR /opt/keycloak

# Copy custom providers
COPY --chown=keycloak:keycloak keycloak/target/custom-mappers.jar /opt/keycloak/providers/

# Build the optimized image
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:26.3.1

COPY --from=builder /opt/keycloak/ /opt/keycloak/

# Set the entrypoint
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
```

### Dockerfile for Configuration Application

```dockerfile
FROM eclipse-temurin:21-jre-alpine

WORKDIR /opt/keycloak-config

# Copy the configuration JAR
COPY java-configuration/target/java-configuration-*.jar java-configuration.jar

# Copy wait script
COPY java-configuration/src/main/scripts/wait-for-keycloak.sh /opt/keycloak-config/

RUN chmod +x /opt/keycloak-config/wait-for-keycloak.sh

# Configure TLS certificate path
ENV CERT_PATH=/mnt/certificates

ENTRYPOINT ["/opt/keycloak-config/wait-for-keycloak.sh"]
```

## Environment Variables

### Core Keycloak Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `KEYCLOAK_ADMIN` | Admin username | `admin` |
| `KEYCLOAK_ADMIN_PASSWORD` | Admin password | `admin123` |
| `KC_DB` | Database vendor | `mysql`, `postgres` |
| `KC_DB_URL` | JDBC URL | `jdbc:mysql://host:3306/db` |
| `KC_DB_USERNAME` | DB username | `keycloak` |
| `KC_DB_PASSWORD` | DB password | `password` |
| `KC_HOSTNAME` | Public hostname | `keycloak.example.com` |
| `KC_HOSTNAME_ADMIN` | Admin hostname | `admin.keycloak.example.com` |
| `KC_HOSTNAME_STRICT` | Strict hostname | `false` |
| `KC_PROXY` | Proxy mode | `edge`, `reencrypt`, `passthrough` |
| `KC_HTTP_ENABLED` | Enable HTTP | `true` |
| `KC_HEALTH_ENABLED` | Enable health endpoints | `true` |
| `KC_METRICS_ENABLED` | Enable metrics | `true` |

### Configuration Application Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `KEYCLOAK_CONFIG_SERVER_URI` | Keycloak URL | `http://keycloak:8080` |
| `KEYCLOAK_HEALTH_URL` | Health endpoint | `http://keycloak:8080/health/ready` |
| `KEYCLOAK_CONFIG_REALM` | Admin realm | `master` |
| `DISABLE_TLS_VERIFICATION` | Skip TLS verify | `true` |

### Azure AD Variables

| Variable | Description |
|----------|-------------|
| `AZURE_CLIENT_ID` | Azure app client ID |
| `AZURE_CLIENT_SECRET` | Azure app secret |
| `AZURE_TENANT_ID` | Azure tenant ID |
| `AZURE_ADMIN_GROUP_ID` | Admin group object ID |
| `AZURE_2NDLINE_GROUP_ID` | 2nd line group object ID |
| `AZURE_1STLINE_GROUP_ID` | 1st line group object ID |

### Custom Provider Variables

| Variable | Description |
|----------|-------------|
| `FLEXII_DB_URL` | Flexii database JDBC URL |
| `FLEXII_DB_USER` | Flexii database username |
| `FLEXII_DB_PASSWORD` | Flexii database password |
| `OISTER_DB_URL` | Oister database JDBC URL |
| `OISTER_DB_USER` | Oister database username |
| `OISTER_DB_PASSWORD` | Oister database password |
| `ENABLE_DB_INITIALIZATION` | Enable DB connections | `true`/`false` |

## TLS/SSL Configuration

### Certificate Mounting in Kubernetes

```yaml
spec:
  containers:
    - name: app
      volumeMounts:
        - name: certs
          mountPath: /mnt/certificates
          readOnly: true
  volumes:
    - name: certs
      secret:
        secretName: keycloak-tls
```

### SSL Context Utility

```java
public class SSLContextUtil {
    private static final String[] CERT_FILES = {
        "tls.crt", "ca.crt", "server.crt", "certificate.crt", "ca-bundle.crt"
    };
    private static final Path CERT_PATH = Paths.get("/mnt/certificates");
    
    public static Optional<SSLContext> getCustomSSLContext() {
        if (!Files.exists(CERT_PATH)) {
            return Optional.empty();
        }
        
        for (String certFile : CERT_FILES) {
            Path certPath = CERT_PATH.resolve(certFile);
            if (Files.exists(certPath)) {
                return Optional.of(createSSLContext(certPath));
            }
        }
        return Optional.empty();
    }
    
    private static SSLContext createSSLContext(Path certPath) {
        // Load certificate and create SSLContext
        CertificateFactory cf = CertificateFactory.getInstance("X.509");
        X509Certificate cert = (X509Certificate) cf.generateCertificate(
            new FileInputStream(certPath.toFile())
        );
        
        KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
        ks.load(null, null);
        ks.setCertificateEntry("keycloak", cert);
        
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(
            TrustManagerFactory.getDefaultAlgorithm()
        );
        tmf.init(ks);
        
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(null, tmf.getTrustManagers(), null);
        return sslContext;
    }
}
```

### Wait Script with TLS Support

```bash
#!/bin/bash
set -e

CURL_TLS_OPTIONS=""

# Check for mounted certificates
if [ -d "/mnt/certificates" ]; then
    for cert_file in /mnt/certificates/*; do
        if [ -f "$cert_file" ]; then
            CURL_TLS_OPTIONS="--cacert $cert_file"
            break
        fi
    done
fi

# Fallback: disable TLS verification
if [ -z "$CURL_TLS_OPTIONS" ] && [[ "$KEYCLOAK_HEALTH_URL" =~ ^https:// ]]; then
    CURL_TLS_OPTIONS="-k"
fi

# Wait for Keycloak
MAX_ATTEMPTS=60
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    ATTEMPT=$((ATTEMPT+1))
    if curl -s -f -m 10 $CURL_TLS_OPTIONS "$KEYCLOAK_HEALTH_URL" > /dev/null 2>&1; then
        echo "Keycloak is ready!"
        break
    fi
    sleep 5
done

# Run configuration
exec java -jar /opt/keycloak-config/java-configuration.jar
```
