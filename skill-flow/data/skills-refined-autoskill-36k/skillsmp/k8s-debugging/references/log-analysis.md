# 로그 분석 가이드

## 기본 로그 명령어

### 실시간 로그

```bash
# 단일 Pod
kubectl logs <pod> -n eco2 -f

# 모든 컨테이너
kubectl logs <pod> -n eco2 --all-containers -f

# 특정 컨테이너
kubectl logs <pod> -n eco2 -c <container> -f

# 라벨 셀렉터
kubectl logs -l app=chat-worker -n eco2 -f
```

### 이전 로그

```bash
# 재시작 전 로그
kubectl logs <pod> -n eco2 --previous

# 마지막 N줄
kubectl logs <pod> -n eco2 --tail=100

# 시간 기반
kubectl logs <pod> -n eco2 --since=1h
kubectl logs <pod> -n eco2 --since-time="2024-01-01T00:00:00Z"
```

---

## 멀티 Pod 로그

### stern (권장)

```bash
# 설치
brew install stern

# 패턴 매칭
stern "chat-worker.*" -n eco2

# 컨테이너 필터
stern "chat-worker.*" -n eco2 -c main

# 시간 포함
stern "chat-worker.*" -n eco2 -t

# JSON 출력
stern "chat-worker.*" -n eco2 -o json
```

### kubectl 조합

```bash
# 여러 Pod 동시 (background)
for pod in $(kubectl get pods -n eco2 -l app=chat-worker -o name); do
  kubectl logs $pod -n eco2 -f &
done

# 정지: kill %1 %2 ...
```

---

## 구조화된 로그 분석

### JSON 로그 파싱

```bash
# jq로 필터링
kubectl logs <pod> -n eco2 | jq 'select(.level == "error")'

# 특정 필드 추출
kubectl logs <pod> -n eco2 | jq '{time: .timestamp, msg: .message, error: .error}'

# 에러 카운트
kubectl logs <pod> -n eco2 | jq 'select(.level == "error")' | wc -l
```

### 일반 패턴

```bash
# ERROR 라인만
kubectl logs <pod> -n eco2 | grep -i error

# 특정 job_id
kubectl logs <pod> -n eco2 | grep "job_id=abc123"

# 시간대별 필터 (타임스탬프 있는 경우)
kubectl logs <pod> -n eco2 | grep "2024-01-01T10:"
```

---

## Eco² 컴포넌트별 로그

### chat-worker

```bash
# LangGraph 실행 로그
kubectl logs -l app=chat-worker -n eco2 | grep "graph_execution"

# 의도 분류 결과
kubectl logs -l app=chat-worker -n eco2 | grep "intent_classified"

# gRPC 호출
kubectl logs -l app=chat-worker -n eco2 | grep "grpc"
```

### event-router

```bash
# XREADGROUP 소비
kubectl logs -l app=event-router -n eco2 | grep "consumed"

# Pub/Sub 발행
kubectl logs -l app=event-router -n eco2 | grep "published"

# Pending 복구
kubectl logs -l app=event-router -n eco2 | grep "reclaimed"
```

### sse-gateway

```bash
# 연결 수립
kubectl logs -l app=sse-gateway -n eco2 | grep "connection_established"

# 이벤트 전송
kubectl logs -l app=sse-gateway -n eco2 | grep "event_sent"

# 연결 종료
kubectl logs -l app=sse-gateway -n eco2 | grep "connection_closed"
```

---

## 에러 추적

### Exception 추적

```bash
# Python traceback
kubectl logs <pod> -n eco2 | grep -A 20 "Traceback"

# 최근 에러
kubectl logs <pod> -n eco2 --since=10m | grep -i "error\|exception\|failed"
```

### 특정 요청 추적

```bash
# job_id로 추적
JOB_ID="abc123"
kubectl logs -l app=chat-worker -n eco2 | grep "$JOB_ID"
kubectl logs -l app=event-router -n eco2 | grep "$JOB_ID"
kubectl logs -l app=sse-gateway -n eco2 | grep "$JOB_ID"
```

---

## 로그 수집 도구

### 임시 로그 저장

```bash
# 파일로 저장
kubectl logs <pod> -n eco2 > pod-logs.txt

# 시간 범위 저장
kubectl logs <pod> -n eco2 --since=1h > last-hour.txt

# 모든 Pod
for pod in $(kubectl get pods -n eco2 -o name); do
  name=$(echo $pod | cut -d'/' -f2)
  kubectl logs $pod -n eco2 > "${name}.log"
done
```

### 로그 집계

```bash
# 에러 빈도
kubectl logs -l app=chat-worker -n eco2 --since=1h | \
  grep -i error | \
  sort | uniq -c | sort -rn | head -10

# 응답 시간 분석 (latency 필드 있는 경우)
kubectl logs <pod> -n eco2 | \
  jq 'select(.latency != null) | .latency' | \
  sort -n | \
  awk '{sum+=$1; count++} END {print "avg:", sum/count, "ms"}'
```

---

## 유용한 alias

```bash
# ~/.bashrc 또는 ~/.zshrc
alias kl='kubectl logs'
alias klf='kubectl logs -f'
alias kla='kubectl logs --all-containers'
alias klp='kubectl logs --previous'

# 사용
kl <pod> -n eco2
klf <pod> -n eco2
```
