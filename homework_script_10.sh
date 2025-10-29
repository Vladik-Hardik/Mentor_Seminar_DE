#!/bin/bash

dir=$1
[ -z "$dir" ] && echo "Ошибка: укажите директорию" && exit 1

log_file="$dir/sort_log.txt"
mkdir -p "$dir/Images" "$dir/Documents"

echo "Запуск сортировки: $(date '+%Y-%m-%d %H:%M:%S')" >> "$log_file"

for file in "$dir"/*; do
    if [ -f "$file" ]; then
        ext=$(echo "${file##*.}" | tr '[:upper:]' '[:lower:]')
        case "$ext" in
            jpg|png|gif)
                mv "$file" "$dir/Images/"
                echo "Перемещен в Images: $file" >> "$log_file"
                ;;
            txt|pdf|docx)
                mv "$file" "$dir/Documents/"
                echo "Перемещен в Documents: $file" >> "$log_file"
                ;;
        esac
    fi
done

echo "Завершено: $(date '+%H:%M:%S')" >> "$log_file"
echo "" >> "$log_file"
