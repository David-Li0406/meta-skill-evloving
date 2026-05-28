# Pod 트러블슈팅 가이드

## Pod 상태별 진단

### CrashLoopBackOff

```bash
# 원인 파악
kubectl describe pod <pod> -n eco2 | grep -A 20 "State:"
kubectl logs <pod> -n eco2 --previous

# 일반적인 원인
# 1. 애플리케이션 오류 (로그 확인)
# 2. 환경변수/설정 누락
# 3. 의존 서비스 연결 실패
# 4. 리소스 부족 (OOMKilled)

# OOMKilled 확인
kubectl describe pod <pod> -n eco2 | grep -i "oom"
```

### ImagePullBackOff

```bash
# 이미지 정보 확인
kubectl describe pod <pod> -n eco2 | grep "Image:"

# 원인
# 1. 이미지 이름/태그 오류
# 2. Private registry 인증 실패
# 3. 네트워크 문제

# Secret 확인 (private registry)
kubectl get secret -n eco2
kubectl describe secret <registry-secret> -n eco2
```

### Pending

```bash
# 스케줄링 실패 원인
kubectl describe pod <pod> -n eco2 | grep -A 10 "Events:"

# 일반적인 원인
# 1. 리소스 부족 (CPU/Memory)
# 2. Node selector 불일치
# 3. PVC 바인딩 실패
# 4. Taint/Toleration 불일치

# 노드 리소스 확인
kubectl describe nodes | grep -A 10 "Allocated resources"
kubectl top nodes
```

### Terminating (stuck)

```bash
# 강제 삭제
kubectl delete pod <pod> -n eco2 --grace-period=0 --force

# Finalizer 확인/제거
kubectl get pod <pod> -n eco2 -o json | jq '.metadata.finalizers'
kubectl patch pod <pod> -n eco2 -p '{"metadata":{"finalizers":null}}'
```

---

## 리소스 문제

### OOMKilled

```bash
# 메모리 사용량 확인
kubectl top pod <pod> -n eco2

# 리소스 제한 확인
kubectl describe pod <pod> -n eco2 | grep -A 5 "Limits:"

# 해결: limits 증가
kubectl set resources deployment/<name> -n eco2 --limits=memory=1Gi
```

### CPU Throttling

```bash
# CPU 사용량 확인
kubectl top pod <pod> -n eco2

# Throttling 확인 (cgroup)
kubectl exec <pod> -n eco2 -- cat /sys/fs/cgroup/cpu/cpu.stat

# 해결: requests/limits 조정
```

---

## 환경 설정 문제

### 환경변수 확인

```bash
# Pod 환경변수 전체
kubectl exec <pod> -n eco2 -- env

# 특정 환경변수
kubectl exec <pod> -n eco2 -- printenv REDIS_URL

# ConfigMap 확인
kubectl get configmap <name> -n eco2 -o yaml
```

### Secret 확인

```bash
# Secret 목록
kubectl get secrets -n eco2

# Secret 내용 (base64 디코딩)
kubectl get secret <name> -n eco2 -o jsonpath='{.data.password}' | base64 -d
```

### Volume Mount 확인

```bash
# Volume 상태
kubectl describe pod <pod> -n eco2 | grep -A 20 "Volumes:"

# PVC 상태
kubectl get pvc -n eco2
kubectl describe pvc <name> -n eco2
```

---

## Liveness/Readiness 문제

### Probe 실패 확인

```bash
# 이벤트 확인
kubectl describe pod <pod> -n eco2 | grep -i "unhealthy"

# Probe 설정 확인
kubectl get pod <pod> -n eco2 -o yaml | grep -A 10 "livenessProbe:"
```

### 수동 Health Check

```bash
# 컨테이너 내부에서 헬스체크
kubectl exec <pod> -n eco2 -- curl -s localhost:8000/health

# 외부에서 (port-forward)
kubectl port-forward <pod> 8000:8000 -n eco2
curl localhost:8000/health
```

---

## Init Container 문제

```bash
# Init container 상태
kubectl describe pod <pod> -n eco2 | grep -A 20 "Init Containers:"

# Init container 로그
kubectl logs <pod> -n eco2 -c <init-container-name>

# 일반적인 원인
# 1. 의존 서비스 미준비
# 2. 설정 파일 생성 실패
# 3. 권한 문제
```

---

## 재시작 전략

```bash
# Deployment 재시작 (rolling)
kubectl rollout restart deployment/<name> -n eco2

# 특정 Pod 재시작
kubectl delete pod <pod> -n eco2

# Rollout 상태 확인
kubectl rollout status deployment/<name> -n eco2

# 이전 버전 롤백
kubectl rollout undo deployment/<name> -n eco2
```

---

## 유용한 스크립트

### Pod 상태 요약

```bash
#!/bin/bash
# pod-status.sh
NS=${1:-eco2}

echo "=== Pod Status ==="
kubectl get pods -n $NS -o wide

echo ""
echo "=== Recent Events ==="
kubectl get events -n $NS --sort-by='.lastTimestamp' | tail -10

echo ""
echo "=== Resource Usage ==="
kubectl top pods -n $NS 2>/dev/null || echo "Metrics not available"
```

### 문제 Pod 자동 탐지

```bash
#!/bin/bash
# find-issues.sh
NS=${1:-eco2}

echo "=== Non-Running Pods ==="
kubectl get pods -n $NS --field-selector=status.phase!=Running

echo ""
echo "=== Pods with Restarts ==="
kubectl get pods -n $NS -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[0].restartCount}{"\n"}{end}' | awk '$2 > 0'
```
