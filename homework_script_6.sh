#!/bin/bash

#Читает данные из файла input.txt.

cat input.txt

#Перенаправляет вывод команды wc -l (подсчет строк) в файл output.txt

wc -l < input.txt > output.txt

#Перенаправляет ошибки выполнения команды ls для несуществующего файла в файл error.log.

ls nonexistent_file 2> error.log
