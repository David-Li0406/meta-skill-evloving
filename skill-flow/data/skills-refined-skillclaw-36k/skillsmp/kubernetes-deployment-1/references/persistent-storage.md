# Kubernetes Persistent Storage Implementation Guide

## Overview
This guide provides detailed information about implementing persistent storage in Kubernetes, particularly for applications that require data persistence across pod restarts and deployments. This is essential for databases, file storage, and any application that needs to maintain state.

## When to Use Persistent Storage

Use persistent storage when:
- Deploying databases (PostgreSQL, MySQL, MongoDB, etc.)
- Applications that need to store user uploads or files
- Applications that maintain state across restarts
- Applications that need to share data between pods
- Any scenario where data must survive pod lifecycle events

## Kubernetes Storage Concepts

### PersistentVolume (PV)
- Cluster resource representing a piece of storage in the cluster
- Can be backed by various storage systems (NFS, cloud storage, local storage)
- Managed by cluster administrators

### PersistentVolumeClaim (PVC)
- Request for storage by a user/application
- Specifies storage requirements (size, access mode, storage class)
- Bound to a PV by the system

### StorageClass
- Defines different classes of storage
- Enables dynamic provisioning of PVs
- Common classes: fast SSD, standard HDD, premium storage

## Access Modes

- `ReadWriteOnce` (RWO): Single node read-write access
- `ReadOnlyMany` (ROX): Multiple nodes read-only access
- `ReadWriteMany` (RWX): Multiple nodes read-write access
- `ReadWriteOncePod` (RWOP): Single pod read-write access (Kubernetes 1.22+)

## Implementation Patterns

### 1. Basic PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
  namespace: app-namespace
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  # Use specific storage class or leave empty for default
  storageClassName: standard
```

### 2. Using PVC in a Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-storage
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-with-storage
  template:
    metadata:
      labels:
        app: app-with-storage
    spec:
      containers:
      - name: app-container
        image: your-app:latest
        volumeMounts:
        - name: app-storage
          mountPath: /data
        - name: logs-storage
          mountPath: /app/logs
      volumes:
      - name: app-storage
        persistentVolumeClaim:
          claimName: app-storage
      - name: logs-storage
        persistentVolumeClaim:
          claimName: logs-storage
```

### 3. StatefulSet with Persistent Storage (Recommended for Databases)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-db
spec:
  serviceName: postgres-service
  replicas: 1
  selector:
    matchLabels:
      app: postgres-db
  template:
    metadata:
      labels:
        app: postgres-db
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "taskflow_db"
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: db-user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: db-password
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
      storageClassName: standard
```

## Best Practices for Persistent Storage

### 1. Storage Class Selection
- Use default storage class for development environments
- Choose appropriate storage class for performance requirements in production
- Consider cost vs. performance trade-offs

### 2. Capacity Planning
- Estimate storage requirements based on application needs
- Plan for growth over time
- Consider backup and snapshot requirements

### 3. Backup and Recovery
- Implement regular backup strategies
- Test restore procedures
- Consider using Velero for cluster-wide backups

### 4. Security Considerations
- Limit access to storage volumes
- Encrypt sensitive data at rest when possible
- Use appropriate RBAC for storage operations

## Troubleshooting Common Issues

### PVC remains in Pending state
- Check if requested storage class exists and is available
- Verify there's enough available storage in the cluster
- Check if there are any storage quotas limiting the request

### Pod fails to start with storage error
- Verify PVC is bound to a PV
- Check if storage is accessible from the node where pod is scheduled
- Verify appropriate permissions for storage access

### Data not persisting across pod restarts
- Ensure using StatefulSet for stateful applications
- Verify volume mounts are correctly configured
- Check if storage is being wiped during container startup

## Minikube Specific Considerations

### Default Storage Class
Minikube comes with a default storage class that provisions from the Minikube VM's disk space. Ensure sufficient disk space is allocated when starting Minikube:

```bash
minikube start --disk-size=20g
```

### Dynamic Provisioning
Minikube uses the hostpath provisioner for dynamic storage provisioning, which creates directories on the host filesystem.

### Storage Limits
Be mindful of the total disk space available in the Minikube VM when requesting storage.

## Implementation for Taskflow Application

For the Taskflow application, persistent storage should be implemented for:

1. **PostgreSQL Database**:
   - Use StatefulSet with volumeClaimTemplates
   - Request sufficient storage for data growth
   - Configure appropriate resource limits

2. **File Storage** (if needed):
   - For user uploads or file attachments
   - Consider using a separate PVC for file storage
   - Implement proper cleanup procedures

### PostgreSQL Persistent Storage Example

```yaml
# PostgreSQL StatefulSet with persistent storage
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {{ include "taskflow.fullname" . }}-postgres
  labels:
    {{- include "taskflow.labels" . | nindent 4 }}
    app: postgres
spec:
  serviceName: {{ include "taskflow.fullname" . }}-postgres-headless
  replicas: 1
  selector:
    matchLabels:
      {{- include "taskflow.selectorLabels" . | nindent 6 }}
      app: postgres
  template:
    metadata:
      labels:
        {{- include "taskflow.selectorLabels" . | nindent 8 }}
        app: postgres
    spec:
      containers:
      - name: postgres
        image: "postgres:15-alpine"
        imagePullPolicy: IfNotPresent
        ports:
        - name: postgres
          containerPort: 5432
          protocol: TCP
        env:
        - name: POSTGRES_DB
          value: {{ .Values.postgresql.database | quote }}
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: {{ include "taskflow.fullname" . }}-secrets
              key: db-user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ include "taskflow.fullname" . }}-secrets
              key: db-password
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        livenessProbe:
          exec:
            command:
            - sh
            - -c
            - pg_isready -h 127.0.0.1 -p 5432 -U {{ .Values.postgresql.user }}
          initialDelaySeconds: 60
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - sh
            - -c
            - pg_isready -h 127.0.0.1 -p 5432 -U {{ .Values.postgresql.user }}
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          {{- toYaml .Values.postgresql.resources | nindent 12 }}
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes:
        - {{ .Values.persistence.accessMode | quote }}
      resources:
        requests:
          storage: {{ .Values.postgresql.persistence.size | quote }}
      {{- if .Values.persistence.storageClass }}
      {{- if (eq "-" .Values.persistence.storageClass) }}
      storageClassName: ""
      {{- else }}
      storageClassName: {{ .Values.persistence.storageClass }}
      {{- end }}
      {{- end }}
```

## Monitoring and Maintenance

### Storage Usage
Monitor storage usage with:
- `kubectl describe pvc <pvc-name>` to check current usage
- `kubectl get pv,pvc` to see all storage resources
- Implement alerts for storage threshold breaches

### Cleanup Procedures
- Implement data retention policies
- Regular cleanup of temporary files
- Plan for storage expansion as needed

This guide provides the foundation for implementing persistent storage in Kubernetes applications, with specific considerations for the Taskflow application and local Minikube development environments.
