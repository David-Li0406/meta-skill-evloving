# Git Internals: Under the Hood (2026)

Understanding how Git stores data allows for more effective debugging and recovery.

## 1. The Content-Addressable Store

Git is essentially a persistent map of `SHA-256` keys to "objects."

-   **Blobs**: File contents.
-   **Trees**: Directory structures (pointing to blobs and other trees).
-   **Commits**: Snapshots of the tree with metadata (author, message, parent).

## 2. Object Identification (SHA-256)

In 2026, we are migrating from SHA-1 to SHA-256 for better collision resistance and security.

-   *Command*: `git cat-file -p <hash>` to inspect any object.

## 3. The Index (Staging Area)

The index is a binary file (`.git/index`) that prepares the next commit. It is the "bridge" between the working directory and the repository.

-   *Pro Tip*: Use `git ls-files --stage` to see exactly what's in the index.

## 4. References and Symbolic Refs

-   **Heads**: Local branches (`refs/heads/`).
-   **Remotes**: Remote tracking branches (`refs/remotes/`).
-   **HEAD**: A symbolic ref pointing to the current branch or commit.

## 5. Packfiles and Garbage Collection

Git compresses objects into "packfiles" to save space.
-   `git gc`: Runs cleanup and optimization.
-   `git prune`: Removes unreachable objects.

---
*Updated: January 22, 2026 - 19:05*
