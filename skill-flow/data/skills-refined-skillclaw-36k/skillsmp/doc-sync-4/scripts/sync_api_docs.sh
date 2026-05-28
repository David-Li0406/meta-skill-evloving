#!/bin/bash
# API Documentation Sync Script
# Updates API.md with current routes and controller information

OUTPUT_FILE=".claude/API.md"

echo "🔄 Syncing API documentation..."

# Generate timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")

# Get routes
echo "📋 Extracting routes..."
ROUTES=$(rails routes --expanded 2>/dev/null || echo "Error: Could not generate routes")

# Start building documentation
cat > "$OUTPUT_FILE" << 'EOF'
# API Routes Documentation

EOF

echo "**Last Updated**: $TIMESTAMP" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Add routes table
echo "## Routes Overview" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo '| HTTP | Path | Controller#Action | 설명 |' >> "$OUTPUT_FILE"
echo '|------|------|-------------------|------|' >> "$OUTPUT_FILE"

# Parse routes and format as table
rails routes | grep -v "^rails_" | grep -v "^turbo_" | while IFS= read -r line; do
    # Parse route line (format: Prefix Verb URI Pattern Controller#Action)
    if [[ $line =~ ([A-Z]+)[[:space:]]+(/[^[:space:]]+)[[:space:]]+([^#]+#[^[:space:]]+) ]]; then
        VERB="${BASH_REMATCH[1]}"
        PATH="${BASH_REMATCH[2]}"
        CONTROLLER="${BASH_REMATCH[3]}"

        # Generate description based on controller action
        DESCRIPTION=$(echo "$CONTROLLER" | awk -F'#' '{
            controller=$1
            action=$2

            if (action == "index") print "목록 조회"
            else if (action == "show") print "상세 조회"
            else if (action == "new") print "생성 폼"
            else if (action == "create") print "생성"
            else if (action == "edit") print "수정 폼"
            else if (action == "update") print "수정"
            else if (action == "destroy") print "삭제"
            else print "-"
        }')

        echo "| $VERB | $PATH | $CONTROLLER | $DESCRIPTION |" >> "$OUTPUT_FILE"
    fi
done

# Add controller sections
echo "" >> "$OUTPUT_FILE"
echo "## Controller Details" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# List all controllers
for controller in app/controllers/*_controller.rb; do
    if [[ -f "$controller" ]] && [[ ! "$controller" =~ application_controller ]]; then
        controller_name=$(basename "$controller" .rb)
        class_name=$(echo "$controller_name" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g')

        echo "### $class_name" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"

        # Extract actions
        actions=$(grep -E "^\s*def\s+" "$controller" | sed 's/def //' | sed 's/$//' | tr '\n' ', ' | sed 's/, $//')

        if [ -n "$actions" ]; then
            echo "**Actions**: $actions" >> "$OUTPUT_FILE"
        fi

        # Check for before_actions
        before_actions=$(grep -E "before_action" "$controller" | head -3)
        if [ -n "$before_actions" ]; then
            echo "" >> "$OUTPUT_FILE"
            echo "**Filters**:" >> "$OUTPUT_FILE"
            echo '```ruby' >> "$OUTPUT_FILE"
            echo "$before_actions" >> "$OUTPUT_FILE"
            echo '```' >> "$OUTPUT_FILE"
        fi

        echo "" >> "$OUTPUT_FILE"
        echo "---" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

# Add authentication section
cat >> "$OUTPUT_FILE" << 'EOF'

## Authentication

현재 프로젝트는 세션 기반 인증을 사용합니다.

**로그인 확인**:
```ruby
before_action :require_login

def require_login
  unless current_user
    redirect_to login_path
  end
end
```

**권한 확인**:
```ruby
before_action :authorize_user

def authorize_user
  redirect_to root_path unless @resource.user == current_user
end
```

## Response Formats

기본적으로 HTML 응답을 반환합니다.

**Success**:
- Redirect with flash message (Korean)
- Example: `redirect_to @post, notice: '성공적으로 생성되었습니다.'`

**Error**:
- Re-render form with `status: :unprocessable_entity`
- Errors available in form via `@resource.errors`

EOF

echo "✅ API documentation updated: $OUTPUT_FILE"
echo ""
echo "📊 Summary:"
echo "  - Routes documented: $(grep -c "^|" "$OUTPUT_FILE" || echo 0)"
echo "  - Controllers documented: $(find app/controllers -name "*_controller.rb" ! -name "application_controller.rb" | wc -l)"
