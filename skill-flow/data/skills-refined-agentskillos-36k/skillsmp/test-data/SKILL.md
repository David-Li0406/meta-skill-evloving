---
name: test-data
description: Read and write test data
---
# Database access use SqlCmd.exe too

## Tools
- **SqlCmd.exe**: for database access
- **server**: -S "(local)\DEV2022"
- **Trust Server Certificate**: -C
- **trusted connection**: -E 
- **database**: -d "MotoRent"

## Database 
- **MotoRent**: for tenant, contains user data, such as `Shop`, `Vehicle` etc. an d core objecs such as `User`, `Organization` etc.

## Tenant schema
- **MotoRent** is multi-tenant application, where each tenant has it's own schema, the list of all tenants is kept in `Core.Organization` table.
- **Tenant**: Take `Shop` as example, it's table name is `Shop`, and it's schema name is `<tenant>`

## JSON object
- **JSON** column is for serialized JSON data .Net object,as described in `MotoRent.Domain` project
- **Entity** JSON data is a serialized object of `Entity` class, `MotoRent.Domain.Entities.<table>`, where `<table>` is the `Entity`
- **Primary key** `<table>Id` format


## Interview
- **Interview** use AskUserQuestion tools
- **Tenant** ask me about the tenant if one not specified, account