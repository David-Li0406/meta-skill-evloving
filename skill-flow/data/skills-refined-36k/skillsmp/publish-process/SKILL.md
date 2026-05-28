---
name: Publish Process
description: Workflow for publishing dataforge packages (annotation, generator) in the correct order.
---

# Publish Process
1. 发布前保证 所有  test passed
2. 只更改 changelog.md 和 pubspec.yaml 里的 version 字段
2. 不要删除 dependency_overrides。 
1. 先更新版本号。只改动 version: xxx 。其他的依赖版本不要改
2. 始终保持  cli 和 generator 的   `dataforge_annotation:` 和 `dataforge_base` 版本为空,
2. 始终保持  dataforge_base   `dataforge_annotation:`  版本为空,
2. 编写 changelog
3. 使用 `dart compile exe cli/bin/dataforge_cli.dart -o cli/dataforge-${version}` 编译一个 产物
3. 按顺序发布 
    a. dataforge_annotation
    b. dataforge_base
	b. dataforge_cli
	c. dataforge_generator
4. 发布代码： fd pub publish   执行后等待一会 输入 y
5. 发布结束后，执行 git add . && git commit -m  "publish version:xx"
