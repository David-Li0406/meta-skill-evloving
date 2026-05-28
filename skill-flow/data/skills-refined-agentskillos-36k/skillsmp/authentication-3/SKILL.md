---
name: authentication
description: Support Authentication with JWS and local Signer
---
---
name: UI
description: Support UI
---

## role
 - You are an expert Staff engineer who works with nextJS.
 - you write clean, understandable code with good documentation.
 - you ensure good visablity on the console so that any issues can be easily understood and fixed
 - You have great UX skills
 - you place different functionality in logical places in the UI with easy access
 
 ## style
  - this app should match the sytle of https://www.crossriver.com/
  - keep the UI friendly and calm, but pleasant and happy (within the above style)
  - prefer using tailwindcss

## page setup
  - the user should not have to scroll to see things (unless the output of a prompt is big)  
  - there should be a clear menu, matching the style of the above link
  - if a user has to login during some interaction, you do NOT lose any user data in any fields while the user logs in, after logging in, you return to the page he was on.
  - all fields relevant to do the current action should be easily available
  - setting should be in a settings menu
  - going from one page to another does NOT lose any data

## menu
 - the menu will support logout
 - settings 
 - prompts
 - for admins - update/add agents

## login
  - after a normal login you go to the main page (the prompt page)
  - if there is a need to login during an interaction, the user will be asked to login and then he will return to the requested page with all the data, e.g. if sending a prompt requires login, then the user logs in, the prompt is sent to the backend and the user is redirected (if needed) to the page with the output. He will not lose any data

## toolstack
 - next
- react
- react-dom

- @tailwindcss/postcss
- @types/node
- @types/react
- @types/react-dom
- eslint
- eslint-config-next
- tailwindcss
- typescript
