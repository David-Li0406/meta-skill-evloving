---
name: bedrock
description: Support Bedrock
---

# defining an agent
- All agents will be described by a json file in the configuration folder
- the json file will contain all data required to define agents
- the app will ensure that the agents deployed have the features as defined in the configuration
- the app will ensure that all agents are "prepared" and have an alias, which will be in the configuration file
- when creating an agent, any data that needs to be in the configuration file but is missing will be added by the app
  e.g. the alias id given by bedrock
- while interacting with bedrock, the app will write to the console what it is doing and when each step finishes, with a report of success or fail. If the step fails, there will be a clear message explaining what the problem is (e.g. missing permission, missing field x ...)  

# load time
 - the app will ensure that the json file describing the agents is valid. 
 - if there is some definition of a new agent that has missing fields, since they need to be populated by the app, 
   those fields will contain the word MISSING. 
 - if there are any fields containing the word MISSING, the app will ensure that the field is updated with a real value. 
   The value may be the result of some action that the app must take.
- if anything is missing in the configuration file, the app will abort explaining what the issue is.
- if there is a problem updating some field, the app will abort with a full desciption of the issue.


# Examples
[AgentConfiguration.md](AgentConfiguration.md) - sample of expected agent configuration, before an admin adds new agents