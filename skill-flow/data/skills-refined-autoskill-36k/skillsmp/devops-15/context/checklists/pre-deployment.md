# Pre-Deployment Checklist

## Overview
This checklist ensures all necessary steps are completed before deploying to staging or production. Use this systematically to reduce deployment risks and ensure readiness.

## Code Quality and Testing

### Test Coverage
- [ ] All tests passing in CI/CD pipeline
- [ ] Unit test coverage meets threshold (typically 80%+)
- [ ] Integration tests executed successfully
- [ ] E2E tests passing for critical user flows
- [ ] No flaky tests in test suite
- [ ] Performance tests completed (if applicable)
- [ ] Load tests completed for high-traffic features

### Code Review
- [ ] Pull request approved by required reviewers
- [ ] All review comments addressed
- [ ] Code follows project style guidelines
- [ ] No TODO or FIXME comments for critical issues
- [ ] Technical debt documented if introduced

### Security
- [ ] Security scans completed (SAST, dependency audit)
- [ ] No critical or high-severity vulnerabilities
- [ ] Medium vulnerabilities reviewed and accepted or fixed
- [ ] Container images scanned for vulnerabilities
- [ ] Secrets not committed to repository
- [ ] API keys and credentials rotated if needed
- [ ] Authentication and authorization tested

## Database and Data

### Database Migrations
- [ ] Database migrations tested in staging environment
- [ ] Migrations are backward compatible (if needed)
- [ ] Migration rollback tested and documented
- [ ] Migration execution time measured (< 5 min for production)
- [ ] Database backup completed before migration
- [ ] Data migration script validated (if applicable)
- [ ] Index creation for new columns planned

### Data Integrity
- [ ] Data validation rules tested
- [ ] Existing data compatibility verified
- [ ] Data migration plan documented
- [ ] Data backup recovery tested
- [ ] Foreign key constraints validated

## Infrastructure and Configuration

### Infrastructure Changes
- [ ] Infrastructure as code changes reviewed
- [ ] Terraform/CloudFormation plan reviewed
- [ ] Resource limits appropriate (CPU, memory, disk)
- [ ] Auto-scaling configured correctly
- [ ] Network policies and security groups updated
- [ ] DNS changes prepared (if applicable)
- [ ] SSL certificates valid and up to date

### Configuration
- [ ] Environment variables documented
- [ ] Configuration changes reviewed
- [ ] Secrets uploaded to secret management system
- [ ] Feature flags configured
- [ ] Third-party API credentials validated
- [ ] Service dependencies configured
- [ ] Logging levels appropriate for environment

## Deployment Preparation

### Build and Artifacts
- [ ] Build completed successfully
- [ ] Docker image built and tagged correctly
- [ ] Image pushed to container registry
- [ ] Artifact version tagged (git tag or semantic version)
- [ ] Build artifacts scanned for vulnerabilities
- [ ] Deployment manifest/configuration prepared

### Deployment Strategy
- [ ] Deployment strategy selected (rolling, blue-green, canary)
- [ ] Deployment order documented for microservices
- [ ] Traffic routing plan documented
- [ ] Rollback plan documented and tested
- [ ] Deployment window scheduled (if required)
- [ ] Maintenance mode prepared (if needed)

## Monitoring and Observability

### Monitoring Setup
- [ ] Monitoring dashboards exist for new features
- [ ] Key metrics identified and instrumented
- [ ] Health check endpoints functional
- [ ] Alerts configured for critical metrics
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Logging configured and tested
- [ ] APM/tracing configured (if applicable)

### Alert Configuration
- [ ] Critical alerts configured with correct thresholds
- [ ] Alert recipients configured
- [ ] Runbooks linked in alert annotations
- [ ] Alert channels tested (PagerDuty, Slack, etc.)
- [ ] Escalation policy defined
- [ ] On-call schedule confirmed

## Communication and Documentation

### Team Communication
- [ ] Deployment scheduled and communicated to team
- [ ] Stakeholders notified of deployment
- [ ] Customer support team briefed on changes
- [ ] User-facing changes documented
- [ ] Known issues documented
- [ ] Deployment timeline shared

### Documentation
- [ ] Release notes prepared
- [ ] API changes documented
- [ ] Configuration changes documented
- [ ] Runbooks updated
- [ ] Architecture diagrams updated (if changed)
- [ ] User documentation updated (if applicable)

## Dependencies and External Services

### Service Dependencies
- [ ] Dependent services are healthy and available
- [ ] External API integrations tested
- [ ] Third-party service status verified
- [ ] Rate limits for external APIs verified
- [ ] Fallback mechanisms tested
- [ ] Circuit breakers configured

### Capacity and Performance
- [ ] Expected load calculated
- [ ] Capacity planning completed
- [ ] Database connection pool sized appropriately
- [ ] Cache warmed (if applicable)
- [ ] CDN configuration updated (if applicable)
- [ ] Rate limiting configured

## Rollback Preparation

### Rollback Plan
- [ ] Rollback procedure documented
- [ ] Previous stable version identified
- [ ] Rollback tested in staging
- [ ] Rollback criteria defined (when to rollback)
- [ ] Database rollback plan documented (if needed)
- [ ] Quick rollback commands prepared
- [ ] Team knows how to execute rollback

### Backup and Recovery
- [ ] Database backup completed and verified
- [ ] Configuration backup saved
- [ ] Previous version artifacts accessible
- [ ] Recovery time objective (RTO) understood
- [ ] Recovery point objective (RPO) acceptable

## Compliance and Governance

### Compliance
- [ ] Regulatory requirements met (GDPR, HIPAA, etc.)
- [ ] Data privacy requirements addressed
- [ ] Audit logging configured for sensitive operations
- [ ] Compliance documentation updated
- [ ] Change management approval obtained (if required)

### Sign-offs
- [ ] Technical lead approval
- [ ] Product owner approval (if required)
- [ ] Security team approval (for high-risk changes)
- [ ] Operations team notified
- [ ] Business stakeholders informed

## Final Checks

### Pre-Deployment Smoke Test
- [ ] Application starts successfully in staging
- [ ] Health check endpoints return healthy status
- [ ] Critical user flows functional in staging
- [ ] Database connectivity verified
- [ ] External API integrations working
- [ ] Authentication/authorization working
- [ ] Static assets loading correctly

### Deployment Readiness
- [ ] Deployment scripts tested
- [ ] Deployment automation verified
- [ ] Access credentials available
- [ ] VPN/network access confirmed
- [ ] Deployment tools installed and configured
- [ ] Team members available during deployment
- [ ] Incident response team on standby

### Risk Assessment
- [ ] Deployment risk level assessed (low, medium, high)
- [ ] Risk mitigation strategies in place
- [ ] Blast radius identified and minimized
- [ ] Customer impact assessed
- [ ] Business impact assessed
- [ ] Deployment timing appropriate (avoid peak hours for high-risk)

## Environment-Specific Checks

### Staging Deployment
- [ ] Staging environment matches production
- [ ] Test data prepared
- [ ] Smoke tests passing
- [ ] Performance acceptable
- [ ] No critical errors in logs

### Production Deployment
- [ ] Staging deployment successful
- [ ] Staging has been stable for 24+ hours
- [ ] Production maintenance window scheduled (if needed)
- [ ] Customer notification sent (if downtime expected)
- [ ] Status page updated (if applicable)
- [ ] Emergency contacts available
- [ ] War room/communication channel prepared

## Special Considerations

### First Deployment
- [ ] Infrastructure provisioned
- [ ] Domain/DNS configured
- [ ] SSL certificates installed
- [ ] Monitoring infrastructure set up
- [ ] Logging infrastructure set up
- [ ] Initial data seeded

### Major Version Upgrade
- [ ] Breaking changes documented
- [ ] Migration path documented
- [ ] Backward compatibility strategy defined
- [ ] Phased rollout plan prepared
- [ ] Extended monitoring period planned

### Hotfix Deployment
- [ ] Issue severity verified
- [ ] Fix tested thoroughly
- [ ] Impact of not deploying understood
- [ ] Deployment can be fast-tracked
- [ ] Team available for support

## Checklist Completion

### Final Verification
- [ ] All critical items checked
- [ ] All blockers resolved
- [ ] Risk level acceptable
- [ ] Team confident in deployment
- [ ] Go/no-go decision made

### Sign-off
- Deployment Prepared By: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Approved By: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Risk Levels

**Low Risk:**
- Bug fixes with no infrastructure changes
- Configuration changes with known impact
- Non-customer-facing changes
- Easy rollback available

**Medium Risk:**
- New features with moderate complexity
- Database schema changes (backward compatible)
- Infrastructure changes with testing
- Multiple service deployments

**High Risk:**
- Breaking API changes
- Database migrations affecting large datasets
- Major architecture changes
- First-time deployments
- Changes affecting critical business flows

---

## Notes

Use this space to document any specific considerations for this deployment:

```
[Deployment-specific notes]
```

---

**Remember:** It's better to delay a deployment than to deploy with unresolved critical issues. When in doubt, postpone and investigate.
