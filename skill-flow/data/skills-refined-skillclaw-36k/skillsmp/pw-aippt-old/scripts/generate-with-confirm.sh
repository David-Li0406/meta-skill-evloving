#!/bin/bash
# generate-with-confirm.sh - 边确认边生成 PPT 图片
#
# 用法: bash generate-with-confirm.sh [项目目录]
# 示例: bash generate-with-confirm.sh /path/to/aippt-project

PROJECT_DIR="${1:-.}"
PROMPTS_DIR="$PROJECT_DIR/prompts"
IMAGES_DIR="$PROJECT_DIR/images"

# 检查目录
if [ ! -d "$PROMPTS_DIR" ]; then
  echo "错误: 提示词目录不存在 - $PROMPTS_DIR"
  exit 1
fi

# 创建输出目录
mkdir -p "$IMAGES_DIR"

# 获取所有提示词文件
PROMPT_FILES=($(ls "$PROMPTS_DIR"/*.md 2>/dev/null | sort))

if [ ${#PROMPT_FILES[@]} -eq 0 ]; then
  echo "错误: 未找到提示词文件"
  exit 1
fi

echo "找到 ${#PROMPT_FILES[@]} 个提示词文件"
echo ""

# 逐个处理
for i in "${!PROMPT_FILES[@]}"; do
  FILE="${PROMPT_FILES[$i]}"
  FILENAME=$(basename "$FILE")
  NUM=$((i + 1))
  TOTAL=${#PROMPT_FILES[@]}

  echo "============================================================"
  echo "任务 $NUM/$TOTAL: $FILENAME"
  echo "============================================================"
  echo ""

  # 询问用户
  read -p "是否生成此图像? (y/n/q, 默认: y): " answer
  answer=${answer:-y}

  case "$answer" in
    y|Y)
      echo "生成中..."
      # 临时创建目录结构
      TEMP_DIR=$(mktemp -d)
      mkdir -p "$TEMP_DIR/prompts"
      cp "$FILE" "$TEMP_DIR/prompts/"

      # 调用生成脚本 (输出目录是 TEMP_DIR)
      (cd "$TEMP_DIR" && echo "y" | node ~/.claude/skills/pw-image-generation/scripts/generate-image.js . 2>&1) | grep -E "(生成|成功|失败|错误|保存)" || true

      # 查找生成的图片
      GENERATED_IMAGE=$(find "$TEMP_DIR" -name "*.png" -type f | head -1)

      if [ -n "$GENERATED_IMAGE" ]; then
        # 使用原始文件名
        OUTPUT_NAME="$(basename "$FILE" .md).png"
        mv "$GENERATED_IMAGE" "$IMAGES_DIR/$OUTPUT_NAME"
        echo "✓ 已生成: $IMAGES_DIR/$OUTPUT_NAME"
      else
        echo "✗ 生成失败"
      fi

      # 清理临时目录
      rm -rf "$TEMP_DIR"
      ;;
    q|Q)
      echo "用户取消,退出"
      exit 0
      ;;
    *)
      echo "跳过"
      ;;
  esac

  echo ""
done

echo "============================================================"
echo "完成! 共处理 ${#PROMPT_FILES[@]} 个文件"
echo "============================================================"
