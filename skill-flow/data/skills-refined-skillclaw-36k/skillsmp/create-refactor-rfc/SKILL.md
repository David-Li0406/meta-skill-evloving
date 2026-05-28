---
name: create-refactor-rfc
description: Use this skill to create an RFC for a refactor.
---

This skill will be invoked when the user wants to create an RFC for a refactor. Follow the steps below:

1. Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions.

2. Explore the repo to understand the current state of the codebase and in what ways the codebase violates the values.

3. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

4. Interview the user about changes they would like to see made. Be extremely detailed and thorough.

5. Create a RFC for the changes that will be made. The RFC should be structured like so:

<rfc-template>

## Problem Statement

The problem that the developer is facing, from the developer's perspective. This should be readable by a newcomer to the project.

## Solution

The solution to the problem, from the developer's perspective.

## Implementation

This section should explain the rough API changes (internal and external), package changes, etc. The goal is to give an idea to reviews about the subsystems that require change and the surface area of those changes.

## Behaviors

A LONG, numbered list of user stories. Each user story should be in the format of:

1. <feature-or-module>: <description-of-behavior>

<user-story-example>
1. Clip Reducer: When an ADD_CLIP action is dispatched, the clip is added to the state with a unique ID.
</user-story-example>

Do NOT suggest an ordering of the tasks. The ordering will be determined later based on priority.

This list of user stories should be extremely extensive and cover all aspects of the refactor.

</rfc-template>

5. Submit the RFC as a GitHub issue.
