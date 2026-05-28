# Examples

**Example: Stand up an ADK Agent Engine runtime**
- Inputs: `project_id`, `region`, desired model, and whether Code Execution + Memory Bank are enabled.
- Outputs: Terraform resources for the runtime + IAM + VPC/PSC, plus validation commands to confirm the agent is reachable and permissions are correct.