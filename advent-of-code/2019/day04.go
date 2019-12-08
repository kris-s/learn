package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

func main() {
	var input string
	_, err := fmt.Scan(&input)
	bounds := strings.Split(input, "-")

	lower, err := strconv.Atoi(bounds[0])
	upper, err := strconv.Atoi(bounds[1])
	fmt.Println(lower, upper)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Part One:", passwordCount(lower, upper, partOneValidPassword))
	fmt.Println("Part Two:", passwordCount(lower, upper, partTwoValidPassword))
}

func passwordCount(lower, upper int, valid func(int) bool) int {
	count := 0
	for i := lower + 1; i < upper; i++ {
		if valid(i) {
			count++
		}
	}
	return count
}

func partOneValidPassword(password int) bool {
	rule1 := hasAdjacentPair(password)
	rule2 := digitsIncrease(password)
	return rule1 && rule2
}

func partTwoValidPassword(password int) bool {
	rule1 := hasAdjacentIsolatedPair(password)
	rule2 := digitsIncrease(password)
	return rule1 && rule2
}

func hasAdjacentPair(password int) bool {
	passRunes := []rune(strconv.Itoa(password))
	for i := 0; i < len(passRunes)-1; i++ {
		if passRunes[i] == passRunes[i+1] {
			return true
		}
	}
	return false
}

func hasAdjacentIsolatedPair(password int) bool {
	passRunes := []rune(strconv.Itoa(password))
	for i := 0; i < len(passRunes)-2; i++ {
		if passRunes[i] == passRunes[i+1] && passRunes[i+1] != passRunes[i+2] {
			if i == 0 || passRunes[i-1] != passRunes[i] {
				return true
			}
		}
	}

	// check last two runes
	return passRunes[len(passRunes)-2] == passRunes[len(passRunes)-1] &&
		passRunes[len(passRunes)-2] != passRunes[len(passRunes)-3]
}

func digitsIncrease(password int) bool {
	passRunes := []rune(strconv.Itoa(password))

	for i := 0; i < len(passRunes)-1; i++ {
		if passRunes[i+1] >= passRunes[i] {
			continue
		} else {
			return false
		}
	}
	return true
}
