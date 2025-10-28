#!/bin/bash
read -p "Введите путь к файлу: " file
if [-f "$file"]; then
	echo "Файл найден!"
else
	echo "Файл не найден."
fi

