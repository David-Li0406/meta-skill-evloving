# functions-transforms: 변환 함수

## 도메인 조회

```javascript
lsp({ operation: 'describe', domain: 'transforms' })
```

## 사용 방법

변환 함수는 `write` 또는 `edit` 도구로 CAD 코드에 포함하여 실행합니다.

```javascript
// write로 전체 코드 작성 → 자동 실행
write({
  file: 'main',
  code: `
    drawRect('box', 100, 100, 50, 50);
    translate('box', 200, 0);
    rotate('box', Math.PI / 4);
  `
});

// edit로 부분 수정 → 자동 실행
edit({
  file: 'main',
  old_code: "translate('box', 200, 0);",
  new_code: "translate('box', 300, 100);"
});
```

**실행 중 오류 발생 시:** 자동 롤백되어 이전 상태 복원

## translate

도형을 이동합니다. **값이 누적됩니다** (절대 위치가 아닌 상대 이동).

```javascript
translate(name, dx, dy, options?): boolean
```

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| name | string | - | 엔티티/그룹 이름 |
| dx | number | - | X 이동량 |
| dy | number | - | Y 이동량 |
| options.space | 'world' \| 'local' | 'world' | 좌표계 |

**반환값:** `boolean` - 성공 시 `true`, 실패 시 `false`

```javascript
translate('box', 100, 50);              // 월드 좌표로 이동
translate('box', 10, 0, { space: 'local' });  // 로컬 좌표로 이동
```

## rotate

도형을 회전합니다. **각도가 누적됩니다** (절대 회전이 아닌 상대 회전).

```javascript
rotate(name, angle, options?): boolean
```

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| name | string | - | 엔티티/그룹 이름 |
| angle | number | - | 회전 각도 (**라디안**) |
| options.space | 'world' \| 'local' | 'world' | 좌표계 |

**반환값:** `boolean` - 성공 시 `true`, 실패 시 `false`

```javascript
rotate('box', Math.PI / 4);     // 45도 회전
rotate('box', Math.PI / 2);     // 90도 회전
rotate('box', Math.PI);         // 180도 회전
```

**각도 변환:**
- 45° = `Math.PI / 4`
- 90° = `Math.PI / 2`
- 180° = `Math.PI`
- 360° = `Math.PI * 2`

## scale

크기 조절. **값이 누적됩니다** (절대 스케일이 아닌 상대 스케일).

```javascript
scale(name, sx, sy, options?): boolean
```

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| name | string | - | 엔티티/그룹 이름 |
| sx | number | - | X 스케일 (1.0 = 원본) |
| sy | number | - | Y 스케일 (1.0 = 원본) |
| options.space | 'world' \| 'local' | 'world' | 좌표계 |

**반환값:** `boolean` - 성공 시 `true`, 실패 시 `false`

```javascript
scale('box', 2, 2);             // 2배 확대
scale('box', 0.5, 0.5);         // 절반 축소
scale('box', 1, 2);             // Y만 2배 (늘리기)
```

**⚠️ 그룹 자식에 scale 적용 시:**

```javascript
// ✅ 반드시 space: 'local' 사용
scale('child_entity', 1.2, 1.2, { space: 'local' });

// ❌ 기본값 'world'는 부모 변환 영향받아 위치도 변함
scale('child_entity', 1.2, 1.2);  // 의도와 다른 결과!
```

## setPivot

피벗(회전 중심) 설정

```javascript
setPivot(name, px, py): boolean
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| name | string | 엔티티 이름 |
| px | number | 피벗 X (로컬 좌표) |
| py | number | 피벗 Y (로컬 좌표) |

**반환값:** `boolean` - 성공 시 `true`, 실패 시 `false`

```javascript
// 왼쪽 아래를 중심으로 회전
setPivot('door', -10, -20);
rotate('door', Math.PI / 4);
```

## deleteEntity

엔티티를 삭제합니다.

```javascript
deleteEntity(name): boolean
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| name | string | 삭제할 엔티티 이름 |

**반환값:** `boolean` - 성공 시 `true`, 엔티티가 없거나 실패 시 `false`

```javascript
deleteEntity('old_box');
```

**참고:** 존재하지 않는 엔티티를 삭제하면 `false`를 반환합니다 (에러 발생 안 함).

---

## Utility 함수 (utility 도메인)

다음 함수들은 `transforms` 도메인이 아닌 `utility` 도메인에 속합니다.

```javascript
lsp({ operation: 'describe', domain: 'utility' })
```

## duplicate

엔티티를 복제합니다.

```javascript
duplicate(sourceName, newName): boolean
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| sourceName | string | 원본 엔티티 이름 |
| newName | string | 새 엔티티 이름 |

**반환값:** `boolean` - 성공 시 `true`, 실패 시 `false`

```javascript
duplicate('tree', 'tree_copy');
translate('tree_copy', 50, 0);
```

## mirror

엔티티를 미러 복제합니다.

```javascript
mirror(sourceName, newName, axis): boolean
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| sourceName | string | 원본 엔티티 이름 |
| newName | string | 새 엔티티 이름 |
| axis | 'x' \| 'y' | 미러 축 |

**반환값:** `boolean` - 성공 시 `true`, 실패 시 `false`

```javascript
// Y축 기준 미러 (좌우 반전)
mirror('left_arm', 'right_arm', 'y');

// X축 기준 미러 (상하 반전)
mirror('top_half', 'bottom_half', 'x');
```
