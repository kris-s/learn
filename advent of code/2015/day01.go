package main

import (
	"fmt"
	"log"
)

func main() {
	var input string
	if _, err := fmt.Scanf("%s", &input); err != nil {
		log.Fatal(err)
	}

	floor := 0

	for i, rune := range input {
		if rune == '(' {
			floor++
		} else if rune == ')' {
			floor--
		}
		if floor == -1 {
			fmt.Println("Entered the basement at", i+1)
		}
	}

	fmt.Println("Floor", floor)
}
