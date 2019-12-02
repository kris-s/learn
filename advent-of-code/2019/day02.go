package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

func main() {
	var input string
	if _, err := fmt.Scan(&input); err != nil {
		log.Fatal(err)
	}
	codes := prep(input)
	codes = intcode(codes)
	fmt.Println("Part one:", codes[0])
	noun, verb := partTwo(prep(input))
	fmt.Println("Part two:", (100*noun)+verb)

}

func prep(s string) []int {
	temp := strings.Split(s, ",")
	nums := []int{}

	for _, num := range temp {
		value, err := strconv.Atoi(num)
		if err != nil {
			log.Fatal(err)
		}
		nums = append(nums, value)
	}

	nums[1] = 12
	nums[2] = 2

	return nums
}

func intcode(codes []int) []int {
	cursor := 0

	for {
		code := codes[cursor]
		switch code {
		case 1:
			aIndex := codes[cursor+1]
			bIndex := codes[cursor+2]
			cIndex := codes[cursor+3]

			a := codes[aIndex]
			b := codes[bIndex]
			codes[cIndex] = a + b
			cursor += 4
		case 2:
			aIndex := codes[cursor+1]
			bIndex := codes[cursor+2]
			cIndex := codes[cursor+3]

			a := codes[aIndex]
			b := codes[bIndex]
			codes[cIndex] = a * b
			cursor += 4
		case 99:
			return codes
		default:
			log.Fatalf("Unknown opcode %d at index %d\n", code, cursor)
		}
	}
}

func partTwo(codes []int) (int, int) {
	workingCopy := make([]int, len(codes))
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			copy(workingCopy, codes)
			workingCopy[1] = noun
			workingCopy[2] = verb
			workingCopy = intcode(workingCopy)
			if workingCopy[0] == 19690720 {
				return noun, verb
			}
		}
	}
	return 0, 0
}
