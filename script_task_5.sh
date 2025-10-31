#!/bin/bash
read -p "Укажите директорию: " dir

for file in "$dir"/*; do
  mv "$file" "$dir/backup_$(basename "$file")"
done

