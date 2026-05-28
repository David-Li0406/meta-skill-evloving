# 네트워크 진단 가이드

## 서비스 연결 확인

### DNS 확인

```bash
# Pod 내부에서 DNS 조회
kubectl exec <pod> -n eco2 -- nslookup redis-streams
kubectl exec <pod> -n eco2 -- nslookup character-api.eco2.svc.cluster.local

# DNS 문제 확인
kubectl exec <pod> -n eco2 -- cat /etc/resolv.conf
```

### 서비스 연결 테스트

```bash
# HTTP 서비스
kubectl exec <pod> -n eco2 -- curl -s http://sse-gateway:8000/health

# gRPC 서비스 (grpcurl 필요)
kubectl exec <pod> -n eco2 -- grpcurl -plaintext character-api:50051 list

# TCP 연결
kubectl exec <pod> -n eco2 -- nc -zv redis-streams 6379

# Redis
kubectl exec <pod> -n eco2 -- redis-cli -h redis-streams ping
```

---

## Port Forward

### 로컬 디버깅

```bash
# 단일 포트
kubectl port-forward <pod> 8000:8000 -n eco2

# 서비스 포워딩
kubectl port-forward svc/sse-gateway 8000:8000 -n eco2

# 백그라운드
kubectl port-forward <pod> 8000:8000 -n eco2 &

# Redis 접속
kubectl port-forward svc/redis-streams 6379:6379 -n eco2
redis-cli -h localhost -p 6379
```

### 여러 포트

```bash
# 동시에 여러 포트
kubectl port-forward <pod> 8000:8000 9090:9090 -n eco2
```

---

## 서비스 메시 진단

### Endpoints 확인

```bash
# 서비스 엔드포인트
kubectl get endpoints -n eco2
kubectl describe endpoints sse-gateway -n eco2

# 서비스 상세
kubectl describe svc sse-gateway -n eco2
```

### Network Policy

```bash
# 네트워크 정책 확인
kubectl get networkpolicy -n eco2
kubectl describe networkpolicy <name> -n eco2

# 정책이 트래픽 차단하는지 확인
# (정책 없으면 기본 허용)
```

---

## 클러스터 내부 통신

### Pod 간 통신

```bash
# Pod IP 확인
kubectl get pod <pod> -n eco2 -o wide

# 다른 Pod에서 직접 접근
kubectl exec <other-pod> -n eco2 -- curl http://<pod-ip>:8000/health
```

### Service Discovery

```bash
# 서비스 DNS 형식
# <service>.<namespace>.svc.cluster.local

# 같은 네임스페이스
kubectl exec <pod> -n eco2 -- curl http://sse-gateway:8000/health

# 다른 네임스페이스
kubectl exec <pod> -n eco2 -- curl http://redis.redis-ns.svc.cluster.local:6379
```

---

## 외부 통신

### Egress 확인

```bash
# 외부 연결 테스트
kubectl exec <pod> -n eco2 -- curl -s https://httpbin.org/ip

# DNS 외부 조회
kubectl exec <pod> -n eco2 -- nslookup google.com
```

### Ingress 확인

```bash
# Ingress 리소스
kubectl get ingress -n eco2
kubectl describe ingress <name> -n eco2

# Ingress Controller 로그
kubectl logs -l app.kubernetes.io/name=ingress-nginx -n ingress-nginx
```

---

## gRPC 연결 디버깅

### grpcurl 사용

```bash
# 서비스 목록
kubectl exec <pod> -n eco2 -- grpcurl -plaintext character-api:50051 list

# 메서드 호출
kubectl exec <pod> -n eco2 -- grpcurl -plaintext \
  -d '{"match_label": "플라스틱"}' \
  character-api:50051 \
  character.CharacterService/GetCharacterByMatch
```

### 연결 상태 확인

```bash
# gRPC 헬스체크
kubectl exec <pod> -n eco2 -- grpcurl -plaintext \
  character-api:50051 \
  grpc.health.v1.Health/Check
```

---

## Redis 연결 디버깅

```bash
# Redis CLI 접속
kubectl exec -it <redis-pod> -n eco2 -- redis-cli

# 원격 Redis 테스트
kubectl exec <pod> -n eco2 -- redis-cli -h redis-streams -p 6379 ping

# 연결 정보
kubectl exec <pod> -n eco2 -- redis-cli -h redis-streams info clients
```

---

## 네트워크 디버그 Pod

```bash
# 디버그용 Pod 생성
kubectl run netshoot --rm -it --image=nicolaka/netshoot -n eco2 -- /bin/bash

# 내부 명령어
# curl, wget, dig, nslookup, nc, tcpdump, iperf 등 사용 가능

# tcpdump 예시 (패킷 캡처)
tcpdump -i any port 6379 -w redis.pcap
```

---

## 일반적인 문제

### Connection Refused

```bash
# 서비스 실행 중인지 확인
kubectl get pods -l app=<service> -n eco2

# 포트 바인딩 확인
kubectl exec <pod> -n eco2 -- netstat -tlnp
```

### Timeout

```bash
# 네트워크 정책 확인
kubectl get networkpolicy -n eco2

# 방화벽/보안그룹 확인 (클라우드)
```

### DNS Resolution Failed

```bash
# CoreDNS 상태
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -l k8s-app=kube-dns -n kube-system

# resolv.conf 확인
kubectl exec <pod> -n eco2 -- cat /etc/resolv.conf
```
