#!/bin/bash
read -p "Укажите директорию: " dir
tar -czvf "$(date +%Y-%m-%d)_${dir##*/}.tar.gz" "$dir"
echo "Архив создан!"

