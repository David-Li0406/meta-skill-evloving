---
name: bash-scripting
description: Instructions in case if any bash (or any shell in general) script is needed.
---

When determining where script is if needed, always use

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if refering something from ROOT directory is needed then define ROOT based on DIR in relative manner from current script like:

ROOT="${DIR}/.."

or

ROOT="${DIR}/../.."

... depends how many directories up we have to go

Don't use shebang at the top of the file.

Call script like this:

/bin/bash ${DIR}/script.sh

When using variables always surround them with ${}.

never $DIR, always ${DIR}

# error handling

Before exit with non zero exit code from script in case of error always print the message what's happened like so:

echo "${0} error: [and then message here]"

this way we will spit out information about origin of the error - when it comes to which script is it.

Add to the message any relevent parameters values like so

"name of env var MY_ENV_VAR=>${MY_ENV_VAR}<"

(surround with ><, this way I will see any whitespaces at the beginning or end of the value)
