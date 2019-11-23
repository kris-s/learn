package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {
	lines := []string{}
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}
	}
	rawLen := len(strings.Join(lines, ""))
	memLen := memLen(lines)
	encLen := encLen(lines)
	fmt.Printf("Part One: %d - %d = %d\n", rawLen, memLen, rawLen-memLen)
	fmt.Printf("Part Two: %d - %d = %d\n", encLen, rawLen, encLen-rawLen)
}

func encLen(lines []string) int {
	count := 0
	for _, line := range lines {
		count += len(line)
		count += strings.Count(line, "\"")
		count += strings.Count(line, "\\")
		// add leading and trailing double quotes
		count += 2
	}
	return count
}

func memLen(lines []string) int {
	count := 0

	for _, line := range lines {
		runes := []rune(line)
		// slice leading and trailing double quotes
		runes = runes[1 : len(runes)-1]

		// double quote 34
		// backslash 92
		// x 120
		cursor := 0
		escaped := []rune{}
		for cursor < len(runes) {
			r := runes[cursor]
			if r == 92 {
				next := runes[cursor+1]
				if next == 92 || next == 34 {
					escaped = append(escaped, next)
					cursor++
				} else if next == 120 {
					escaped = append(escaped, '*')
					cursor++
					cursor++
					cursor++
				}
			} else {
				escaped = append(escaped, r)
			}
			cursor++
		}
		count += len(escaped)
	}

	return count
}
