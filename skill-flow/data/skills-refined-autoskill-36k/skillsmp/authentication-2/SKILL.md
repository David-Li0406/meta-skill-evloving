---
name: authentication
description: Support Authentication with JWS and local Signer
---

# Use self Signed JWT
 - create a Signer when the app loads. It will be different each time the app starts
 - When a user signs in (s)he will get a JWT containing the username + timeout (default 1 hour, but see configuration file)
 - There is a dynamoDB database with an entry for each user, it should reflect if the user is logged in / out
 - The JWT will be in a "header"


 # examples
  .github\skills\authentication\examples\auth.ts - this file contains an example which is similar to what we need
                                                   we do not need a refresh token, but we do need to save to dynamodb
