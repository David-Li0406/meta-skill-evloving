---
name: alm-processing
description: Use this to perform operations on the langgraph4j project.  1) create a new project release
---

# create a new project release

In this project we follow the "git flow" branching strategy. 
To create a new release we need to accomplish the following steps

1. create a ad-hoc release branch with the  command
```
script/start-release.sh <version>
``
2. update project release with the command 
```
script/set-version.sh <version>
```
3. ask to the user when ready to close the release and when it confirm, close the release with command:
```
script/finish-release.sh <version>
```
4. If all goes well generate the CHANGELOG with command:
```
script/hotfix-changelog.sh
```

