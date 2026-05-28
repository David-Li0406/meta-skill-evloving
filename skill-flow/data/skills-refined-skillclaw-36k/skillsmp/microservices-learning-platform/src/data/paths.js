// Learning paths data for content-oriented progression
// Updated to include new critical modules on DDD and Distributed Systems
export const paths = [
  {
    id: 'foundations',
    name: '🏗️ Foundations Path',
    description: 'Start here! Understand when microservices are (and aren\'t) the right choice, learn the theory behind distributed systems, and master service boundary design.',
    modules: [
      'should-you-use-microservices',
      'introduction',
      'distributed-systems',
      'domain-driven-design'
    ],
    focuses: [
      'Decision Making',
      'Distributed Systems Theory',
      'Domain-Driven Design',
      'Service Boundaries'
    ],
    estimatedTime: '4-6 hours',
    isRecommendedStart: true,
  },
  {
    id: 'implementation',
    name: '⚡ Implementation Path',
    description: 'Build your first microservices using NestJS. Learn REST APIs, CRUD operations, and service creation fundamentals.',
    modules: [
      'nestjs-fundamentals',
      'first-microservice'
    ],
    focuses: [
      'NestJS Framework',
      'REST APIs',
      'Service Implementation',
      'Best Practices'
    ],
    estimatedTime: '3-4 hours',
    prerequisites: ['foundations'],
  },
  {
    id: 'communication',
    name: '📡 Communication Path',
    description: 'Master how microservices talk to each other: synchronous (HTTP, gRPC), asynchronous (message queues), and cross-service data access patterns.',
    modules: [
      'communication',
      'database-patterns'
    ],
    focuses: [
      'HTTP & gRPC',
      'Message Queues',
      'Event-Driven Architecture',
      'Data Patterns'
    ],
    estimatedTime: '4-5 hours',
    prerequisites: ['implementation'],
  },
  {
    id: 'infrastructure',
    name: '🐳 Infrastructure Path',
    description: 'Production-ready skills: API Gateway, service discovery, containerization, and security.',
    modules: [
      'api-gateway',
      'service-discovery',
      'docker',
      'authentication'
    ],
    focuses: [
      'API Gateway',
      'Service Discovery',
      'Docker & Containers',
      'Security & Auth'
    ],
    estimatedTime: '5-6 hours',
    prerequisites: ['communication'],
  },
  {
    id: 'production',
    name: '🚀 Production Path',
    description: 'Advanced topics for running microservices in production: Kubernetes, monitoring, resilience, testing, and CI/CD.',
    modules: [
      'kubernetes',
      'monitoring',
      'resilience',
      'testing',
      'cicd',
      'production'
    ],
    focuses: [
      'Kubernetes Orchestration',
      'Observability & Monitoring',
      'Resilience Patterns',
      'CI/CD Pipelines'
    ],
    estimatedTime: '8-10 hours',
    prerequisites: ['infrastructure'],
  },
  {
    id: 'full-curriculum',
    name: '🎓 Complete Curriculum',
    description: 'The full microservices journey from "should I?" to production deployment. All 18 modules for those who want the complete picture.',
    modules: [
      'should-you-use-microservices',
      'introduction',
      'distributed-systems',
      'domain-driven-design',
      'nestjs-fundamentals',
      'first-microservice',
      'communication',
      'database-patterns',
      'api-gateway',
      'service-discovery',
      'docker',
      'authentication',
      'kubernetes',
      'monitoring',
      'resilience',
      'testing',
      'cicd',
      'production'
    ],
    focuses: [
      'Complete Foundation',
      'Implementation Skills',
      'Production Patterns',
      'DevOps & Operations'
    ],
    estimatedTime: '25-30 hours',
    isComprehensive: true,
  }
];

// Quick reference for module difficulty progression
export const moduleOrder = [
  'should-you-use-microservices',  // Module 0 - CRITICAL
  'introduction',                   // Module 1
  'nestjs-fundamentals',            // Module 2
  'distributed-systems',            // Module 3 - CRITICAL
  'domain-driven-design',           // Module 4 - CRITICAL
  'first-microservice',             // Module 5
  'communication',                  // Module 6
  'database-patterns',              // Module 7
  'api-gateway',                    // Module 8
  'service-discovery',              // Module 9
  'docker',                         // Module 10
  'authentication',                 // Module 11
  'kubernetes',                     // Module 12
  'monitoring',                     // Module 13
  'resilience',                     // Module 14
  'testing',                        // Module 15
  'cicd',                           // Module 16
  'production',                     // Module 17
];


