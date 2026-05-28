# Traefik Integration

cert-manager provides TLS certificates for Traefik IngressRoute and Ingress resources.

## Certificate + IngressRoute Pattern

Two-step process: create Certificate resource, reference secret in IngressRoute.

### 1. Certificate Resource

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: myapp-tls
  namespace: default
spec:
  secretName: myapp-tls-secret
  dnsNames:
    - myapp.example.com
    - www.myapp.example.com
  issuerRef:
    name: ca-issuer        # Your ClusterIssuer or Issuer
    kind: ClusterIssuer
```

### 2. IngressRoute with TLS

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: myapp
  namespace: default
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`myapp.example.com`)
      kind: Rule
      services:
        - name: myapp-service
          port: 80
  tls:
    secretName: myapp-tls-secret  # Must match Certificate secretName
```

## Standard Ingress Pattern

For Kubernetes Ingress (not IngressRoute), use annotations:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    cert-manager.io/cluster-issuer: ca-issuer
spec:
  ingressClassName: traefik
  tls:
    - hosts:
        - myapp.example.com
      secretName: myapp-tls-secret
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-service
                port:
                  number: 80
```

Annotation triggers automatic Certificate creation by cert-manager.

## Wildcard Certificates

Single certificate for all subdomains:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard-tls
  namespace: default
spec:
  secretName: wildcard-tls-secret
  dnsNames:
    - "*.example.com"
    - example.com
  issuerRef:
    name: ca-issuer
    kind: ClusterIssuer
```

Reuse secret across multiple IngressRoutes.

## Troubleshooting

### Certificate Not Ready

```bash
kubectl get certificate -n default
kubectl describe certificate myapp-tls -n default
```

Check:
- Issuer exists and is Ready
- dnsNames are valid
- secretName doesn't conflict

### Secret Not Created

```bash
kubectl get secret myapp-tls-secret -n default
kubectl get certificaterequest -n default
```

Check CertificateRequest events for issuer errors.

### TLS Not Working in Traefik

1. Verify secret exists and has `tls.crt` + `tls.key`
2. Check IngressRoute `secretName` matches Certificate `secretName`
3. Ensure `websecure` entrypoint is configured in Traefik
4. Verify namespace - secret must be in same namespace as IngressRoute

### Decode Certificate

```bash
kubectl get secret myapp-tls-secret -n default \
  -o jsonpath='{.data.tls\.crt}' | base64 -d | \
  openssl x509 -text -noout | head -20
```

Check Subject, Issuer, validity dates, and SANs.
