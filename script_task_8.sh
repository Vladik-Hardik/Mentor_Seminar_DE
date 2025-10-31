#!/bin/bash

usage=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

if [ "$usage" -gt 80 ]; then
  echo "Использование диска превышает 80% (${usage}%)!"
else
  echo "Использование ${usage}%."
fi
