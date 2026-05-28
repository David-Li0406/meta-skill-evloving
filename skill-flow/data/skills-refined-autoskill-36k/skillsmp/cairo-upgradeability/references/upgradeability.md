# Upgradeability Reference

Source: https://www.starknet.io/cairo-book/ch103-03-upgradeability.html

## Native upgradeability
- Starknet allows replacing a contract's class hash via `replace_class_syscall`.
- The instance address and storage remain the same.

## Safety
- Upgrade entry points must be protected with access control.
- Validate the new class hash before applying the upgrade.
- Proxy patterns are common for complex upgrade paths.
