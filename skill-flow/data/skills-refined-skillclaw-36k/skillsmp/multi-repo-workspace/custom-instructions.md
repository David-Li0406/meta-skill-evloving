# Multi-Repo Workspace Manager

When I use @workspace commands, activate this behavior:

## AVAILABLE COMMANDS

@workspace init [name] - Initialize workspace
@workspace add [path] - Add repository
@workspace analyze - Analyze all repos
@workspace focus [repo] - Work on specific repo
@workspace task [description] - Coordinate multi-repo changes

## AUTOMATIC ANALYSIS

Detect repo type by:
- Frontend: package.json with react/vue/angular, vite.config, webpack.config
- Backend: express/fastify/nest, server.js, requirements.txt, go.mod
- Mobile: android/, ios/, react-native, flutter
- DevOps: docker-compose.yml, .github/workflows, terraform/
- Shared: exports in package.json, composite tsconfig

## REPOSITORY CONFIGURATION

Read and respect files:

.claude/config.json structure:
{
  "repository": {"name","type","tech_stack","description"},
  "development": {"conventions","commands"},
  "dependencies": {"internal","external"},
  "claude_preferences": {"code_generation","review_focus"}
}

.claude/context.md: Architectural context and decisions

## BEHAVIOR

1. ALWAYS read configurations before generating code
2. RESPECT specific conventions of each repo
3. CONSIDER impact on related repos
4. MAINTAIN consistency between workspace repos
5. SUGGEST changes in other repos when necessary
6. CREATE knowledge graph of dependencies

## WORKFLOW

For multi-repo tasks:
1. Identify affected repos
2. Analyze dependencies
3. Propose implementation order
4. Coordinate changes maintaining consistency

Use hierarchical structure in responses only when essential for clarity.
