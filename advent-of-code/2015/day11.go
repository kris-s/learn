package main

import (
	"fmt"
	"log"
	"strings"
)

func main() {
	var input string
	if _, err := fmt.Scanf("%s", &input); err != nil {
		log.Fatal(err)
	}

	next := nextPassword(input)
	fmt.Println("Part one password:", next)
	fmt.Println("Part two password:", nextPassword(next))
}

func nextPassword(s string) string {
	s = incrementString(s)
	for !validPassword(s) {
		s = incrementString(s)
	}
	return s
}

func validPassword(s string) bool {
	if !hasStraight(s) {
		return false
	}

	if hasIOL(s) {
		return false
	}

	if !hasTwoPair(s) {
		return false
	}

	return true
}

func incrementString(s string) string {
	runes := []rune(s)
	carry := false

	for i := len(runes) - 1; i > -1; i-- {
		if i == len(runes)-1 || carry {
			if runes[i] == 'z' {
				carry = true
				runes[i] = 'a'
			} else {
				runes[i] = runes[i] + 1
				carry = false
			}
		}
	}

	incremented := string(runes)
	if carry {
		incremented = "a" + incremented
	}

	return incremented
}

func hasStraight(s string) bool {
	runes := []rune(s)
	for i, r := range runes {
		if i < len(runes)-3 {
			if runes[i+1] == r+1 && runes[i+2] == r+2 {
				return true
			}
		}
	}
	return false
}

func hasIOL(s string) bool {
	for _, substr := range []string{"i", "o", "l"} {
		if strings.Contains(s, substr) {
			return true
		}
	}
	return false
}

func hasTwoPair(s string) bool {
	runes := []rune(s)
	firstPair := ""
	for i, r := range runes {
		if i < len(runes)-1 {
			if r == runes[i+1] {
				pair := string([]rune{r, runes[i+1]})
				if firstPair == "" {
					firstPair = pair
				} else if pair != firstPair {
					return true
				}
			}
		}
	}
	return false
}
