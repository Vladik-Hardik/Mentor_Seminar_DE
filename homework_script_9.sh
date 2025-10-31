#!/bin/bash

cpu=$(top -bn1 | awk -F'id,' '{split($1,a,","); print 100 - a[length(a)]}' | xargs)
mem=$(free -m | awk '/Mem/{printf("%.0f", $3/$2 * 100)}')
disk=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

echo "CPU: ${cpu}%"
echo "Память: ${mem}%"
echo "Диск: ${disk}%"

if (( mem > 80 )); then
    echo "Память > 80%! Топ процессов:"
    ps -aux --sort=-%mem | head -n 5
else
    echo "Память в норме."
fi
