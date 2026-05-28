#!/bin/bash

# 检查参数
if [ "$#" -lt 2 ]; then
    echo "使用方法: $0 <URL> <名称> [线程数]"
    exit 1
fi

URL=$1
NAME=$2
THREADS=${3:-16}

echo "正在开始下载 '$NAME'..."
echo "链接: $URL"
echo "线程数: $THREADS"

# 执行下载命令
nre "$URL" --save-name "$NAME" --thread-count "$THREADS"

if [ $? -eq 0 ]; then
    echo "下载完成: $NAME"
else
    echo "下载失败: $NAME"
    exit 1
fi
