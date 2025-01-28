#!/bin/bash

if python -m http.server -d ./assets 2>/dev/null; then
    exit 0
fi

if python3 -m http.server -d ./assets 2>/dev/null; then
    exit 0
fi

echo "无法搭建文件服务器：没有检测到命令行python"
echo "Press any key to continue..."
read -n 1 -s
exit 1
