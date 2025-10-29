#!/bin/bash

dir=$1
date=$(date +%Y-%m-%d)
backup_dir="${dir}_backup_${date}"
log_file="backup_log_${date}.txt"
count=0

if [ -z "$dir" ] || [ ! -d "$dir" ]; then
    echo "Ошибка:такой директории нет."
    exit 1
fi

mkdir -p "$backup_dir"

for file in "$dir"/*; do
    if [ -f "$file" ]; then
        cp "$file" "$backup_dir/$(basename "$file")"
        echo "Скопирован: '$file'" >> "$log_file"
        count=$((count + 1))
    fi
done

echo "Скопировано $count файлов" >> "$log_file"
echo "Готово: $count файлов скопировано. Лог: $log_file"
