locals {
  # Account configuration
  aws_account_id = "111111111111"
  account_name   = "myproject-nonprod"
  role_arn       = "arn:aws:iam::111111111111:role/TerraformCrossAccount"

  # Environment
  environment = "non-production"

  # Network configuration (existing VPC)
  vpc_id             = "vpc-xxxxxxxxx"
  private_subnet_ids = ["subnet-priv1", "subnet-priv2", "subnet-priv3"]
  public_subnet_ids  = ["subnet-pub1", "subnet-pub2", "subnet-pub3"]

  # Tags for resources in this account
  tags = {
    Project     = "MyProject"
    Environment = "non-production"
    CostCenter  = "Engineering"
  }
}
