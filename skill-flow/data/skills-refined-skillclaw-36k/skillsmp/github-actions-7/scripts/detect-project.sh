#!/usr/bin/env bash
#
# detect-project.sh - Automatically detect project type and recommend workflows
# Usage: bash detect-project.sh [project-directory]
#

set -e

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"

echo "🔍 Analyzing project in: $PROJECT_DIR"
echo ""

# Detect programming languages
detect_language() {
    if [ -f "package.json" ]; then
        echo "✅ Node.js/TypeScript detected"
        cat package.json | grep -q '"type": "module"' && echo "   - ES modules"
        cat package.json | grep -q '"next"' && echo "   - Next.js"
        cat package.json | grep -q '"react"' && echo "   - React"
        cat package.json | grep -q '"vue"' && echo "   - Vue"
        return 0
    fi

    if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
        echo "✅ Python detected"
        return 0
    fi

    if [ -f "go.mod" ]; then
        echo "✅ Go detected"
        return 0
    fi

    if [ -f "pom.xml" ] || [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
        echo "✅ Java detected"
        [ -f "pom.xml" ] && echo "   - Maven"
        [ -f "build.gradle" ] && echo "   - Gradle"
        return 0
    fi

    echo "❓ No common language detected"
    return 1
}

# Detect containerization
detect_container() {
    if [ -f "Dockerfile" ]; then
        echo "🐳 Docker detected"
        echo "   - Recommended: docker/docker-build-push.yml"
        return 0
    fi
    return 1
}

# Detect Kubernetes
detect_k8s() {
    if [ -d "k8s" ] || [ -d "kubernetes" ] || [ -d "manifests" ]; then
        echo "☸️  Kubernetes detected"
        echo "   - Recommended: kubernetes/k8s-deploy.yml"
        return 0
    fi
    return 1
}

# Detect monorepo setup
detect_monorepo() {
    if [ -f "turbo.json" ]; then
        echo "📦 Turborepo detected"
        echo "   - Recommended: monorepo/monorepo-turbo.yml"
        return 0
    fi

    if [ -f "nx.json" ]; then
        echo "📦 Nx workspace detected"
        echo "   - Recommended: monorepo/monorepo-nx.yml"
        return 0
    fi

    if [ -f "lerna.json" ]; then
        echo "📦 Lerna detected"
        echo "   - Recommended: monorepo/monorepo-path-filter.yml"
        return 0
    fi

    if [ -f "pnpm-workspace.yaml" ]; then
        echo "📦 pnpm workspace detected"
        echo "   - Recommended: monorepo/monorepo-path-filter.yml"
        return 0
    fi

    # Check for multiple package.json files
    PACKAGE_COUNT=$(find . -name "package.json" -type f | wc -l)
    if [ "$PACKAGE_COUNT" -gt 1 ]; then
        echo "📦 Multiple package.json files detected (likely monorepo)"
        echo "   - Recommended: monorepo/monorepo-path-filter.yml"
        return 0
    fi

    return 1
}

# Detect existing workflows
detect_existing_workflows() {
    if [ -d ".github/workflows" ]; then
        WORKFLOW_COUNT=$(ls -1 .github/workflows/*.yml 2>/dev/null | wc -l)
        WORKFLOW_COUNT=$(ls -1 .github/workflows/*.yaml 2>/dev/null | wc -l)
        echo "📁 Existing workflows: $WORKFLOW_COUNT"
        if [ "$WORKFLOW_COUNT" -gt 0 ]; then
            echo "   - Found workflows:"
            ls -1 .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null | sed 's/^/     /'
        fi
        return 0
    fi
    return 1
}

# Main analysis
main() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "       PROJECT ANALYSIS RESULTS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    detect_language
    echo ""

    detect_container
    detect_k8s
    detect_monorepo
    echo ""

    detect_existing_workflows
    echo ""

    # Recommendations
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "       RECOMMENDED WORKFLOWS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    if [ -f "package.json" ]; then
        echo "🔹 basic/nodejs-ci.yml"
        echo "   - Testing, linting, building for Node.js projects"
    fi

    if [ -f "requirements.txt" ]; then
        echo "🔹 basic/python-ci.yml"
        echo "   - Testing, linting, type checking for Python"
    fi

    if [ -f "go.mod" ]; then
        echo "🔹 basic/go-ci.yml"
        echo "   - Building, testing, race detection for Go"
    fi

    if [ -f "Dockerfile" ]; then
        echo "🔹 docker/docker-build-push.yml"
        echo "   - Container builds and registry pushes"
    fi

    if [ -d "k8s" ] || [ -d "kubernetes" ]; then
        echo "🔹 kubernetes/k8s-deploy.yml"
        echo "   - Kubernetes deployments"
    fi

    echo ""
    echo "🔹 security/codeql-analysis.yml"
    echo "   - Static code analysis (recommended for all projects)"
    echo ""
    echo "🔹 security/dependency-review.yml"
    echo "   - Dependency vulnerability scanning"
    echo ""

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "       NEXT STEPS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. Copy recommended workflows:"
    echo "   mkdir -p .github/workflows"
    echo "   cp .claude/skills/github-actions/assets/workflows/[selected].yml .github/workflows/"
    echo ""
    echo "2. Customize workflows for your project"
    echo ""
    echo "3. Commit and push:"
    echo "   git add .github/workflows/"
    echo "   git commit -m \"Add CI/CD workflows\""
    echo "   git push"
    echo ""
    echo "4. Monitor first run in Actions tab"
    echo ""
}

main "$@"
