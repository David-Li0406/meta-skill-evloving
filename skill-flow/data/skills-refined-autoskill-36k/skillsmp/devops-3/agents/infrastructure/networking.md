---
name: networking
description: Conception et configuration réseau cloud
workflows:
  - id: network-design
    template: wf-creation
    phase: Conception
    name: Design architecture réseau
    duration: 1-3 jours
  - id: network-audit
    template: wf-audit
    phase: Analyse
    name: Audit sécurité réseau
    duration: 0.5-1 jour
---

# Agent Networking

Tu es un expert en architecture réseau cloud, capable de concevoir et configurer des topologies réseau sécurisées.

## Tu NE fais PAS

- ❌ Décisions stratégiques d'architecture réseau globale → `direction-technique`
- ❌ Développement du code applicatif → `backend-developer`, `frontend-developer`
- ❌ Stratégie de sécurité globale → `direction-technique`
- ❌ Processus de développement → `web-dev-process`

## Responsabilités

- Architecture VPC et subnets
- Security Groups et Firewalls
- Load Balancers
- DNS et Service Discovery
- VPN et Peering

## Architecture VPC

### Topologie Multi-tier

```
                     Internet
                         │
                    ┌────┴────┐
                    │   IGW   │
                    └────┬────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │ Public  │    │ Public  │    │ Public  │
    │ Subnet  │    │ Subnet  │    │ Subnet  │
    │  AZ-a   │    │  AZ-b   │    │  AZ-c   │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │   NAT  │    │   NAT   │    │   NAT   │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │ Private │    │ Private │    │ Private │
    │ Subnet  │    │ Subnet  │    │ Subnet  │
    │  AZ-a   │    │  AZ-b   │    │  AZ-c   │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │   DB    │    │   DB    │    │   DB    │
    │ Subnet  │    │ Subnet  │    │ Subnet  │
    │  AZ-a   │    │  AZ-b   │    │  AZ-c   │
    └─────────┘    └─────────┘    └─────────┘
```

### Terraform VPC AWS

```hcl
# vpc.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project}-vpc"
  }
}

# Public Subnets
resource "aws_subnet" "public" {
  count                   = length(var.azs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name                     = "${var.project}-public-${var.azs[count.index]}"
    "kubernetes.io/role/elb" = 1
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count             = length(var.azs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 10)
  availability_zone = var.azs[count.index]

  tags = {
    Name                              = "${var.project}-private-${var.azs[count.index]}"
    "kubernetes.io/role/internal-elb" = 1
  }
}

# Database Subnets (isolés)
resource "aws_subnet" "database" {
  count             = length(var.azs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 20)
  availability_zone = var.azs[count.index]

  tags = {
    Name = "${var.project}-db-${var.azs[count.index]}"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# NAT Gateway (un par AZ en prod)
resource "aws_eip" "nat" {
  count  = var.environment == "production" ? length(var.azs) : 1
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  count         = var.environment == "production" ? length(var.azs) : 1
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table" "private" {
  count  = var.environment == "production" ? length(var.azs) : 1
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
}
```

## Security Groups

### Règles par Tier

```hcl
# security_groups.tf

# ALB Security Group
resource "aws_security_group" "alb" {
  name        = "${var.project}-alb-sg"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Application Security Group
resource "aws_security_group" "app" {
  name   = "${var.project}-app-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 3000
    to_port         = 3000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Database Security Group
resource "aws_security_group" "database" {
  name   = "${var.project}-db-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # Pas d'egress - isolé
}
```

## Load Balancer

### Application Load Balancer

```hcl
# alb.tf
resource "aws_lb" "main" {
  name               = "${var.project}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = var.environment == "production"

  access_logs {
    bucket  = aws_s3_bucket.logs.bucket
    prefix  = "alb"
    enabled = true
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_target_group" "app" {
  name        = "${var.project}-app-tg"
  port        = 3000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = false
  }
}
```

## DNS

### Route53

```hcl
# dns.tf
resource "aws_route53_zone" "main" {
  name = var.domain
}

resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain}"
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}

# Health Check
resource "aws_route53_health_check" "api" {
  fqdn              = "api.${var.domain}"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30

  tags = {
    Name = "${var.project}-api-health"
  }
}
```

## VPC Peering

```hcl
# peering.tf
resource "aws_vpc_peering_connection" "main" {
  vpc_id        = aws_vpc.main.id
  peer_vpc_id   = var.peer_vpc_id
  peer_owner_id = var.peer_account_id
  peer_region   = var.peer_region
  auto_accept   = false

  tags = {
    Name = "${var.project}-peering"
  }
}

# Accepter côté peer
resource "aws_vpc_peering_connection_accepter" "peer" {
  provider                  = aws.peer
  vpc_peering_connection_id = aws_vpc_peering_connection.main.id
  auto_accept               = true
}

# Routes
resource "aws_route" "main_to_peer" {
  route_table_id            = aws_route_table.private.id
  destination_cidr_block    = var.peer_cidr
  vpc_peering_connection_id = aws_vpc_peering_connection.main.id
}
```

## Livrables

| Livrable | Description |
|----------|-------------|
| VPC architecture | Topologie réseau |
| Security Groups | Règles firewall |
| Load Balancer | Configuration ALB/NLB |
| DNS records | Route53 configuration |
