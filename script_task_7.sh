#!/bin/bash
add() {
  sum=$(( $1 + $2 ))
  echo "Сумма: $sum"
}
add "$1" "$2"
