# Haskell

**Category**: languages
**Description**: Haskell programming language - purely functional language with strong static typing and lazy evaluation
**Homepage**: https://www.haskell.org

## Package Detection

### HACKAGE
- `base`
- `text`
- `bytestring`
- `containers`
- `aeson`
- `lens`
- `mtl`
- `servant`
- `yesod`

## Configuration Files

- `*.cabal`
- `cabal.project`
- `cabal.project.local`
- `stack.yaml`
- `stack.yaml.lock`
- `package.yaml` (hpack)
- `Setup.hs`
- `.ghci`
- `hie.yaml`
- `fourmolu.yaml`
- `ormolu.yaml`
- `.hlint.yaml`

## File Extensions

- `.hs`
- `.lhs` (literate Haskell)
- `.hsc` (C bindings)
- `.cabal`

## Import Detection

### Haskell
**Pattern**: `^module\s+[\w.]+`
- Module declaration
- Example: `module MyApp.Types where`

**Pattern**: `^import\s+(qualified\s+)?[\w.]+`
- Import statement
- Example: `import qualified Data.Text as T`

**Pattern**: `^data\s+\w+`
- Data type declaration
- Example: `data User = User { name :: Text, age :: Int }`

**Pattern**: `^newtype\s+\w+`
- Newtype declaration
- Example: `newtype UserId = UserId Int`

**Pattern**: `^type\s+\w+`
- Type alias
- Example: `type Handler = ReaderT Config IO`

**Pattern**: `^class\s+\w+`
- Typeclass definition
- Example: `class Monad m => MonadDB m where`

**Pattern**: `::\s*.*->`
- Type signature
- Example: `processData :: Text -> Either Error Result`

## Environment Variables

- `GHC_PACKAGE_PATH`
- `CABAL_DIR`
- `STACK_ROOT`

## Version Indicators

- GHC 9.8 (current)
- GHC 9.6 (stable)
- GHC 9.4 (widely used)
- GHC 8.10 (legacy)

## Detection Notes

- Look for `.hs` files in repository
- .cabal file is primary indicator for Cabal
- stack.yaml indicates Stack build tool
- package.yaml indicates hpack
- Check for src/ and test/ directories

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **.cabal/stack.yaml Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
