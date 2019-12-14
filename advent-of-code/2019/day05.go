package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

func main() {
	input := ""
	_, err := fmt.Scanf("%s", &input)
	if err != nil {
		log.Fatal(err)
	}

	codes1 := []int{}
	codes2 := []int{}
	for _, rawCode := range strings.Split(input, ",") {
		code, err := strconv.Atoi(rawCode)
		if err != nil {
			log.Fatal(err)
		}
		codes1 = append(codes1, code)
		codes2 = append(codes2, code)
	}

	fmt.Println("Part One:")
	intcode(1, codes1)

	fmt.Println("Part Two:")
	intcode(5, codes2)
}

func intcode(input int, codes []int) []int {
	cursor := 0

	for {
		instruction := codes[cursor]
		opcode := instruction % 100
		mode1 := (instruction / 100) % 2
		mode2 := (instruction / 1000) % 2

		mem := input
		switch opcode {
		case 1:
			a, b, c := getParams(cursor, mode1, mode2, codes)
			codes[c] = a + b
			cursor += 4
		case 2:
			a, b, c := getParams(cursor, mode1, mode2, codes)
			codes[c] = a * b
			cursor += 4
		case 3:
			input := mem
			writeAddr := codes[cursor+1]
			codes[writeAddr] = input
			cursor += 2
		case 4:
			readAddr := codes[cursor+1]
			mem = codes[readAddr]
			fmt.Println("Output:", mem)
			cursor += 2
		case 5:
			a, b, _ := getParams(cursor, mode1, mode2, codes)
			if a != 0 {
				cursor = b
			} else {
				cursor += 3
			}
		case 6:
			a, b, _ := getParams(cursor, mode1, mode2, codes)
			if a == 0 {
				cursor = b
			} else {
				cursor += 3
			}
		case 7:
			a, b, c := getParams(cursor, mode1, mode2, codes)

			if a < b {
				codes[c] = 1
			} else {
				codes[c] = 0
			}
			cursor += 4
		case 8:
			a, b, c := getParams(cursor, mode1, mode2, codes)

			if a == b {
				codes[c] = 1
			} else {
				codes[c] = 0
			}
			cursor += 4
		case 99:
			return codes
		default:
			log.Fatalf("Unknown opcode %d at index %d\n", opcode, cursor)
		}
	}
	return codes
}

func getParams(cursor, m1, m2 int, codes []int) (int, int, int) {
	a := codes[cursor+1]
	if m1 == 0 {
		a = codes[a]
	}

	b := codes[cursor+2]
	if m2 == 0 {
		b = codes[b]
	}

	c := codes[cursor+3]
	return a, b, c
}
