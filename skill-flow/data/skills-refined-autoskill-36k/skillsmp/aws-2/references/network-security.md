# AWS Network Security Patterns

## Security Group Patterns

### Web Application (ALB → App → DB)

```yaml
# ALB Security Group - Public facing
ALBSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: ALB - Allow HTTPS from internet
    VpcId: !Ref VPC
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        CidrIp: 0.0.0.0/0
        Description: HTTPS from internet

# App Security Group - Only from ALB
AppSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: App - Only from ALB
    VpcId: !Ref VPC
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 8080
        ToPort: 8080
        SourceSecurityGroupId: !Ref ALBSecurityGroup
        Description: App port from ALB only

# DB Security Group - Only from App
DBSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: DB - Only from App
    VpcId: !Ref VPC
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 5432
        ToPort: 5432
        SourceSecurityGroupId: !Ref AppSecurityGroup
        Description: PostgreSQL from App only
```

### Bastion Host (Use SSM Instead)

```yaml
# AVOID: Bastion with SSH
# BastionSecurityGroup:
#   SecurityGroupIngress:
#     - IpProtocol: tcp
#       FromPort: 22
#       ToPort: 22
#       CidrIp: YOUR_IP/32  # Still risky

# PREFER: SSM Session Manager - No inbound rules needed
AppSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: App with SSM access
    VpcId: !Ref VPC
    # No inbound rules - SSM uses outbound HTTPS
    SecurityGroupEgress:
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        CidrIp: 0.0.0.0/0
        Description: HTTPS for SSM
```

## VPC Design Patterns

### Standard 3-Tier VPC

```yaml
VPC:
  Type: AWS::EC2::VPC
  Properties:
    CidrBlock: 10.0.0.0/16
    EnableDnsHostnames: true
    EnableDnsSupport: true

# Public Subnets (ALB only)
PublicSubnet1:
  Type: AWS::EC2::Subnet
  Properties:
    VpcId: !Ref VPC
    CidrBlock: 10.0.1.0/24
    AvailabilityZone: !Select [0, !GetAZs '']
    MapPublicIpOnLaunch: false  # No auto public IPs!

# Private Subnets (App servers)
PrivateSubnet1:
  Type: AWS::EC2::Subnet
  Properties:
    VpcId: !Ref VPC
    CidrBlock: 10.0.10.0/24
    AvailabilityZone: !Select [0, !GetAZs '']

# Isolated Subnets (Databases)
IsolatedSubnet1:
  Type: AWS::EC2::Subnet
  Properties:
    VpcId: !Ref VPC
    CidrBlock: 10.0.20.0/24
    AvailabilityZone: !Select [0, !GetAZs '']
```

### Route Tables

```yaml
# Public Route Table - Internet Gateway
PublicRouteTable:
  Type: AWS::EC2::RouteTable
  Properties:
    VpcId: !Ref VPC

PublicRoute:
  Type: AWS::EC2::Route
  Properties:
    RouteTableId: !Ref PublicRouteTable
    DestinationCidrBlock: 0.0.0.0/0
    GatewayId: !Ref InternetGateway

# Private Route Table - NAT Gateway
PrivateRouteTable:
  Type: AWS::EC2::RouteTable
  Properties:
    VpcId: !Ref VPC

PrivateRoute:
  Type: AWS::EC2::Route
  Properties:
    RouteTableId: !Ref PrivateRouteTable
    DestinationCidrBlock: 0.0.0.0/0
    NatGatewayId: !Ref NATGateway

# Isolated Route Table - No internet route
IsolatedRouteTable:
  Type: AWS::EC2::RouteTable
  Properties:
    VpcId: !Ref VPC
  # No routes to internet - only VPC local
```

## VPC Flow Logs

```yaml
FlowLog:
  Type: AWS::EC2::FlowLog
  Properties:
    DeliverLogsPermissionArn: !GetAtt FlowLogRole.Arn
    LogGroupName: !Ref FlowLogGroup
    ResourceId: !Ref VPC
    ResourceType: VPC
    TrafficType: ALL  # ACCEPT, REJECT, or ALL
    LogFormat: >-
      ${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr}
      ${srcport} ${dstport} ${protocol} ${packets} ${bytes}
      ${start} ${end} ${action} ${log-status}

FlowLogGroup:
  Type: AWS::Logs::LogGroup
  Properties:
    LogGroupName: /vpc/flow-logs
    RetentionInDays: 30
```

## VPC Endpoints

### Gateway Endpoints (Free)

```yaml
S3Endpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcId: !Ref VPC
    ServiceName: !Sub com.amazonaws.${AWS::Region}.s3
    VpcEndpointType: Gateway
    RouteTableIds:
      - !Ref PrivateRouteTable

DynamoDBEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcId: !Ref VPC
    ServiceName: !Sub com.amazonaws.${AWS::Region}.dynamodb
    VpcEndpointType: Gateway
    RouteTableIds:
      - !Ref PrivateRouteTable
```

### Interface Endpoints (Paid)

```yaml
SecretsManagerEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcId: !Ref VPC
    ServiceName: !Sub com.amazonaws.${AWS::Region}.secretsmanager
    VpcEndpointType: Interface
    SubnetIds:
      - !Ref PrivateSubnet1
      - !Ref PrivateSubnet2
    SecurityGroupIds:
      - !Ref EndpointSecurityGroup
    PrivateDnsEnabled: true

EndpointSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: VPC Endpoint access
    VpcId: !Ref VPC
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        CidrIp: 10.0.0.0/16
        Description: HTTPS from VPC
```

## Network ACLs

```yaml
# Default deny with specific allows
PrivateNACL:
  Type: AWS::EC2::NetworkAcl
  Properties:
    VpcId: !Ref VPC

# Inbound Rules
InboundHTTPSFromVPC:
  Type: AWS::EC2::NetworkAclEntry
  Properties:
    NetworkAclId: !Ref PrivateNACL
    RuleNumber: 100
    Protocol: 6  # TCP
    RuleAction: allow
    CidrBlock: 10.0.0.0/16
    PortRange:
      From: 443
      To: 443

InboundEphemeralFromVPC:
  Type: AWS::EC2::NetworkAclEntry
  Properties:
    NetworkAclId: !Ref PrivateNACL
    RuleNumber: 200
    Protocol: 6
    RuleAction: allow
    CidrBlock: 10.0.0.0/16
    PortRange:
      From: 1024
      To: 65535

# Explicit deny all at end
InboundDenyAll:
  Type: AWS::EC2::NetworkAclEntry
  Properties:
    NetworkAclId: !Ref PrivateNACL
    RuleNumber: 32766
    Protocol: -1
    RuleAction: deny
    CidrBlock: 0.0.0.0/0
```

## WAF Rules

```yaml
WebACL:
  Type: AWS::WAFv2::WebACL
  Properties:
    DefaultAction:
      Allow: {}
    Scope: REGIONAL
    VisibilityConfig:
      CloudWatchMetricsEnabled: true
      MetricName: WebACL
      SampledRequestsEnabled: true
    Rules:
      # AWS Managed Rules
      - Name: AWSManagedRulesCommonRuleSet
        Priority: 1
        OverrideAction:
          None: {}
        Statement:
          ManagedRuleGroupStatement:
            VendorName: AWS
            Name: AWSManagedRulesCommonRuleSet
        VisibilityConfig:
          CloudWatchMetricsEnabled: true
          MetricName: CommonRules
          SampledRequestsEnabled: true

      # SQL Injection Protection
      - Name: AWSManagedRulesSQLiRuleSet
        Priority: 2
        OverrideAction:
          None: {}
        Statement:
          ManagedRuleGroupStatement:
            VendorName: AWS
            Name: AWSManagedRulesSQLiRuleSet
        VisibilityConfig:
          CloudWatchMetricsEnabled: true
          MetricName: SQLiRules
          SampledRequestsEnabled: true

      # Rate Limiting
      - Name: RateLimitRule
        Priority: 3
        Action:
          Block: {}
        Statement:
          RateBasedStatement:
            Limit: 2000
            AggregateKeyType: IP
        VisibilityConfig:
          CloudWatchMetricsEnabled: true
          MetricName: RateLimit
          SampledRequestsEnabled: true
```

## Security Group Audit Queries

```bash
# Find security groups with 0.0.0.0/0
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' \
  --output table

# Find unused security groups
aws ec2 describe-network-interfaces \
  --query 'NetworkInterfaces[].Groups[].GroupId' | sort -u > used.txt
aws ec2 describe-security-groups \
  --query 'SecurityGroups[].GroupId' | sort -u > all.txt
comm -23 all.txt used.txt  # Unused

# Find overly permissive rules
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpProtocol==`-1`]].[GroupId,GroupName]'
```
