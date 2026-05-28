# JSDoc Limitations

## Variable Hover Doesn't Show Type JSDoc

When hovering over a variable, IDEs show the type but NOT the JSDoc from the type's interface. This is [intentional TypeScript behavior](https://github.com/microsoft/TypeScript/issues/37876).

```typescript
/** Player controls. */
interface AudioPlayer {
  /** Whether playing. */
  isPlaying: boolean
}

const player: AudioPlayer = { isPlaying: false }

// Hovering on `player` → shows type only, NO JSDoc
// Hovering on `player.isPlaying` → shows "Whether playing." ✅
// Hovering on `AudioPlayer` → shows "Player controls." ✅
```

__What works:__

* Hover on type name → shows type's JSDoc
* Hover on property access → shows property's JSDoc
* Hover on function call → shows function's JSDoc

__What doesn't work:__

* Hover on variable → only shows type signature, never type's JSDoc

__No workaround__ exists besides adding JSDoc directly to each variable declaration, which violates DRY.
