package main

import (
	"fmt"
	"strconv"
	"strings"
)

func main() {
	fmt.Println("It's time to save Christmas. 🎄")

	fmt.Println(dayOneA(dayOneInput))
	fmt.Println(dayOneB(dayOneInput))
}

func dayOneA(input string) int {
	freq := 0

	for _, val := range strings.Split(input, ", ") {
		v, err := strconv.Atoi(val)
		if err != nil {
			fmt.Println(err)
			continue
		}
		freq += v
	}

	return freq
}

func dayOneB(input string) int {
	freq := 0
	seen := make(map[int]bool)

	for {
		for _, val := range strings.Split(input, ", ") {
			v, err := strconv.Atoi(val)
			if err != nil {
				fmt.Println(err)
				continue
			}
			freq += v

			alreadySeen, _ := seen[freq]
			if alreadySeen {
				return freq
			} else {
				seen[freq] = true
			}
		}
	}
}
