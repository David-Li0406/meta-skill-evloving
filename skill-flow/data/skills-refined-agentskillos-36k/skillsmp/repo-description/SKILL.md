---
name: repo-description
description: mystudy-handsonリポジトリのファイル・ディレクトリを作成・編集する際の背景知識です
---

# Repository Description Skill

## ディレクトリの命名規則

- リポジトリ直下のディレクトリは機能ごとに、`[番号].[サービス名]-[用途]`の命名とする
  - 例: `014.vpc-web-app`
- リポジトリ直下のscripts,srcは各機能で共通的なファイルを格納している

## 機能ごとのディレクトリのファイル構成

- README.mdファイルに構成の説明をしている

**CloudFormationファイル構成**
- 機能ディレクトリ/cfnディレクトリ内にテンプレートファイルを作成すること

**Ansibleファイル構成**
- 機能ディレクトリ/ansibleディレクトリ内にPlaybookファイルを作成すること

**スクリプトファイル構成**
- 機能ディレクトリ/scriptsディレクトリ内にスクリプトファイル（shファイル、pythonファイルなど）を作成すること
- テストファイルは機能ディレクトリ/testsディレクトリに格納すること
  - Pythonファイルの場合はpytest.iniファイルを作成し、pytestからテストできるようにすること

**OpenAPI定義ファイル**
- 機能ディレクトリ/openapiディレクトリ内にOpenAPI定義ファイル（ymlファイル）を作成すること