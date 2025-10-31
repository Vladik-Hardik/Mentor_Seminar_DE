#!/bin/bash

greet_func() {
	echo "Hello, $1"
}

sum_func() {
	echo $(($1+$2))

}

greet_func "Vladik!"
echo "Сумма: $(sum_func 20 5)"
