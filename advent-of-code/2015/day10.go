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

	turns := 50
	lookAndSay(input, turns)
}

func lookAndSay(value string, turns int) {
	fmt.Println(value)
	for i := 0; i < turns; i++ {
		value = nextLookAndSay(value)
		fmt.Println(value, len(value))
	}
}

func nextLookAndSay(value string) string {
	runes := []rune(value)
	type runeCount struct {
		r rune
		c int
	}

	runeCounts := []runeCount{}
	rc := runeCount{runes[0], 1}

	for i, r := range runes {
		// end of the line
		if i == len(runes)-1 {
			runeCounts = append(runeCounts, rc)
			break
		}
		next := runes[i+1]
		if r == next {
			rc.c++
		} else {
			runeCounts = append(runeCounts, rc)
			rc = runeCount{next, 1}
		}
	}

	next := []rune{}
	for _, rc := range runeCounts {
		next = append(next, rune(rc.c)+'0')
		next = append(next, rc.r)
	}
	return string(next)
}
