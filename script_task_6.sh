#!/bin/bash
read -p "Укажите директорию: " dir
find "$dir" -type f -mtime +7 -delete

