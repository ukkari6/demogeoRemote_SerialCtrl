#!/bin/bash

# 出力ディレクトリを指定
OUTPUT_DIR="png_output"

# 出力ディレクトリが存在しない場合は作成
mkdir -p "$OUTPUT_DIR"

# HEICファイルをPNGに変換し、リサイズ
shopt -s nocaseglob  # 大文字小文字を無視するオプションを有効にする
for file in *.heic; do
    # HEICファイルが存在する場合のみ処理
    if [[ -f "$file" ]]; then
        # 一旦PNGに変換
        heif-convert "$file" "${file%.*}.png"

        # PNGを1920x1440にリサイズ
        convert "${file%.*}.png" -resize 1920x1440\> "$OUTPUT_DIR/${file%.*}.png"
        echo "Converted and resized: $file to $OUTPUT_DIR/${file%.*}.png"
        
        # 一時的なPNGファイルを削除
        rm "${file%.*}.png"
    fi
done

# HEICファイルが見つからなかった場合のメッセージ
if [ -z "$(ls *.heic 2>/dev/null)" ]; then
    echo "No HEIC files found."
fi

