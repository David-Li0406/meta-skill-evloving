# Examples

**Example: Deploy a Gemini endpoint + vector search index**
- Inputs: `project_id`, `region`, KMS key (optional), embedding dimensions, and autoscaling bounds.
- Outputs: Terraform for endpoint + deployed model + index, and a smoke test that queries the endpoint and verifies index build status.