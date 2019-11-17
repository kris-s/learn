package main

import (
	"fmt"
	"strings"
)

func main() {
	var count int
	for {
		var input string
		if _, err := fmt.Scanf("%s", &input); err != nil {
			break
		}
		if isNicer(input) {
			count++
		}
	}
	fmt.Println("Nice strings:", count)
}

func isNicer(s string) bool {
	if !containsNonoverlappingPair(s) {
		return false
	}

	if !containsSandwich(s) {
		return false
	}

	return true
}

func isNice(s string) bool {
	if !containsThreeVowels(s) {
		return false
	}

	if !containsDouble(s) {
		return false
	}

	if containsForbidden(s) {
		return false
	}

	return true
}

func containsThreeVowels(s string) bool {
	a := strings.Count(s, "a")
	e := strings.Count(s, "e")
	i := strings.Count(s, "i")
	o := strings.Count(s, "o")
	u := strings.Count(s, "u")

	return (a + e + i + o + u) >= 3
}

func containsDouble(s string) bool {
	runes := []rune(s)
	for i, rune := range runes {
		if i < len(runes)-1 {
			if rune == runes[i+1] {
				return true
			}
		}
	}
	return false
}

func containsForbidden(s string) bool {
	forbidden := []string{"ab", "cd", "pq", "xy"}
	for _, f := range forbidden {
		if strings.Contains(s, f) {
			return true
		}
	}
	return false
}

func containsNonoverlappingPair(s string) bool {
	runes := []rune(s)
	for i, rune := range runes {
		if i < len(runes)-1 {
			pair := fmt.Sprintf("%c%c", rune, runes[i+1])
			if strings.Count(s, pair) >= 2 {
				return true
			}
		}
	}
	return false
}

func containsSandwich(s string) bool {
	runes := []rune(s)
	for i, rune := range runes {
		if i < len(runes)-2 {
			if rune == runes[i+2] {
				return true
			}
		}
	}
	return false
}
