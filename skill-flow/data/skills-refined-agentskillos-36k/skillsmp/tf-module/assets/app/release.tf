# {{APP_NAME}} Helm Release
#
# Uncomment and customize for Helm deployments

# resource "duplocloud_k8_helm_repository" "this" {
#   tenant_id = local.tenant.id
#   name      = local.name
#   url       = "https://charts.example.com"
# }

# resource "duplocloud_k8_helm_release" "this" {
#   tenant_id    = local.tenant.id
#   name         = local.name
#   release_name = local.name
#   interval     = "5m0s"
#   timeout      = "10m0s"
#
#   chart {
#     name               = local.name
#     version            = var.chart_version
#     reconcile_strategy = "ChartVersion"
#     source_type        = "HelmRepository"
#     source_name        = duplocloud_k8_helm_repository.this.name
#   }
#
#   values = jsonencode(yamldecode(templatefile("${path.module}/values.yaml", {
#     namespace = local.tenant.namespace
#     # Add template variables here
#   })))
#
#   depends_on = [duplocloud_k8_helm_repository.this]
# }
