# functions-primitives: 도형 생성 함수

## 도메인 조회

```javascript
lsp({ operation: 'describe', domain: 'primitives' })
```

## drawCircle

원 그리기

```javascript
drawCircle(name, x, y, radius)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| name | string | 엔티티 이름 |
| x | number | 중심 X |
| y | number | 중심 Y |
| radius | number | 반지름 |

```javascript
drawCircle('sun', 0, 100, 30);
```

## drawRect

사각형 그리기

```javascript
drawRect(name, x, y, width, height)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| name | string | 엔티티 이름 |
| x | number | 중심 X |
| y | number | 중심 Y |
| width | number | 너비 |
| height | number | 높이 |

```javascript
drawRect('wall', 0, 20, 50, 40);  // 중심 (0, 20), 50x40
```

## drawLine

선 그리기 (열린 경로)

```javascript
drawLine(name, points)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| name | string | 엔티티 이름 |
| points | number[] | [x1,y1, x2,y2, ...] 좌표 배열 |

```javascript
drawLine('path', [0,0, 10,20, 30,20, 40,0]);
```

## drawPolygon

다각형 그리기 (닫힌 도형)

```javascript
drawPolygon(name, points)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| name | string | 엔티티 이름 |
| points | number[] | [x1,y1, x2,y2, ...] 좌표 배열 |

```javascript
// 삼각형 지붕
drawPolygon('roof', [-25,30, 0,50, 25,30]);

// 오각형
drawPolygon('pentagon', [0,30, -29,9, -18,-24, 18,-24, 29,9]);
```

## drawArc

호 그리기

```javascript
drawArc(name, cx, cy, radius, startAngle, endAngle)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| name | string | 엔티티 이름 |
| cx | number | 중심 X |
| cy | number | 중심 Y |
| radius | number | 반지름 |
| startAngle | number | 시작 각도 (라디안) |
| endAngle | number | 끝 각도 (라디안) |

```javascript
// 반원 (0 ~ π)
drawArc('halfCircle', 0, 0, 50, 0, Math.PI);

// 90도 호
drawArc('quarter', 0, 0, 30, 0, Math.PI / 2);
```

## drawBezier

베지어 곡선 (SVG path 문법)

```javascript
drawBezier(name, path)
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| name | string | 엔티티 이름 |
| path | string | SVG path 문자열 |

```javascript
// 단순 곡선
drawBezier('curve', 'M 0,0 C 10,20 30,20 40,0');

// 닫힌 도형
drawBezier('blob', 'M 0,0 C 20,30 40,30 60,0 C 40,-30 20,-30 0,0 Z');
```

**Path 명령어:**
- `M x,y` - 이동 (Move)
- `L x,y` - 직선 (Line)
- `C cp1x,cp1y cp2x,cp2y x,y` - 3차 베지어 (Cubic)
- `S cp2x,cp2y x,y` - 부드러운 3차 베지어 (Smooth cubic, 이전 제어점 대칭)
- `Q cpx,cpy x,y` - 2차 베지어 (Quadratic)
- `Z` - 경로 닫기

## 좌표계

- **Y+ 위쪽**, 원점 (0,0) 중심
- 모든 좌표는 **중심 기준** (drawRect 포함)
