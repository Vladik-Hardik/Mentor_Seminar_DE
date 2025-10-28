#!/bin/bash
read -p "Введите имя файла: " file
wc -l < "$file"
