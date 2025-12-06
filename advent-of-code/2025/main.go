package main

import (
	"embed"
	"flag"
	"fmt"
	"log"
	"strconv"
	"strings"
)

var dayChoice = flag.Int("d", 1, "day to solve")

//go:embed inputs
var inputs embed.FS

func getInput(filename string) string {
	entries, err := inputs.ReadDir("inputs")
	if err != nil {
		log.Fatal(err)
	}

	for _, entry := range entries {

		if filename == entry.Name() {
			data, err := inputs.ReadFile("inputs/" + filename)
			if err != nil {
				log.Fatal(err)
			}
			return string(data)
		}
	}

	return ""
}

func absInt(value int) int {
	if value < 0 {
		return -value
	} else {
		return value
	}
}

func sumInts(values []int) int {
	result := 0
	for i := range values {
		result += values[i]
	}
	return result
}

func intOrPanic(raw string) int {
	value, err := strconv.Atoi(strings.TrimSpace(raw))
	if err != nil {
		log.Fatal(err)
	}
	return value
}

func main() {
	flag.Parse()

	switch *dayChoice {
	case 1:
		day1("d1s.txt", "d1i.txt")
	case 2:
		day2("d2s.txt", "d2i.txt")
	default:
		fmt.Println("Invalid day choice:", *dayChoice)
	}
}

type Range struct {
	Lower, Upper int
}

func day2(samplefile string, inputfile string) {
	// 1227775554
	day2mirrors(samplefile)
	// 13919717792
	day2mirrors(inputfile)
	// 4174379265
	day2repeats(samplefile)
	// 14582313461
	day2repeats(inputfile)

}

func day2mirrors(filename string) {
	input := getInput(filename)

	ranges := []Range{}

	for _, entry := range strings.Split(input, ",") {
		pair := strings.Split(entry, "-")
		if len(pair) != 2 {
			continue
		}

		lower := intOrPanic(pair[0])
		upper := intOrPanic(pair[1])

		ranges = append(ranges, Range{lower, upper})
	}

	invalid := []int{}

	for _, entry := range ranges {
		for i := entry.Lower; i < entry.Upper; i++ {
			value := strconv.Itoa(i)
			// skip odds
			if len(value)%2 == 1 {
				continue
			}
			half := len(value) / 2

			if value[0:half] == value[half:len(value)] {
				invalid = append(invalid, i)
			}
		}
	}

	fmt.Println("part one:", sumInts(invalid))
}

func day2repeats(filename string) {
	input := getInput(filename)

	ranges := []Range{}

	for _, entry := range strings.Split(input, ",") {
		pair := strings.Split(entry, "-")
		if len(pair) != 2 {
			continue
		}

		lower := intOrPanic(pair[0])
		upper := intOrPanic(pair[1])

		ranges = append(ranges, Range{lower, upper})
	}

	invalid := []int{}

	for _, entry := range ranges {
		for i := entry.Lower; i <= entry.Upper; i++ {
			value := strconv.Itoa(i)

			if !part2valid(value) {
				invalid = append(invalid, i)
			}
		}
	}

	fmt.Println("part two:", sumInts(invalid))
}

func part2valid(value string) bool {
	length := len(value)
	half := length / 2

	if length < 2 {
		return true
	}

	// construct repeating strings from growing slices
	// of the input string
	for i := 1; i <= half; i++ {
		count := length / i
		repeated := strings.Repeat(value[0:i], count)
		if repeated == value {
			return false
		}
	}

	return true
}

func day1(samplefile string, inputfile string) {
	// 3
	day1Dial(samplefile)
	// 1195
	day1Dial(inputfile)
	// 6
	day1Dial2(samplefile)
	// 6770
	day1Dial2(inputfile)
}

func day1Dial(filename string) {
	dial := 50

	input := getInput(filename)
	moves := []int{}

	for _, line := range strings.Split(input, "\n") {
		if strings.HasPrefix(line, "L") {
			s := strings.TrimPrefix(line, "L")
			value := intOrPanic(s)
			value = value % 100
			moves = append(moves, -value)
		} else if strings.HasPrefix(line, "R") {
			s := strings.TrimPrefix(line, "R")
			value := intOrPanic(s)
			value = value % 100
			moves = append(moves, value)
		}
	}

	zeroes := 0

	for _, move := range moves {
		// fmt.Printf("dial: %d, move: %d\n", dial, move)
		dial += move

		if dial > 99 {
			dial -= 100
		} else if dial < 0 {
			dial += 100
		}

		if dial == 0 {
			zeroes++
		}
	}

	fmt.Println("zeroes:", zeroes)
}

func day1Dial2(filename string) {
	dial := 50

	input := getInput(filename)
	moves := []int{}

	for _, line := range strings.Split(input, "\n") {
		if strings.HasPrefix(line, "L") {
			s := strings.TrimPrefix(line, "L")
			value, err := strconv.Atoi(s)
			if err != nil {
				log.Fatal(err)
			}
			moves = append(moves, -value)
		} else if strings.HasPrefix(line, "R") {
			s := strings.TrimPrefix(line, "R")
			value, err := strconv.Atoi(s)
			if err != nil {
				log.Fatal(err)
			}
			moves = append(moves, value)
		}
	}

	zeroes := 0

	for _, move := range moves {
		// fmt.Printf("dial: %d, move: %d\n", dial, move)
		tick := 1
		if move < 0 {
			tick = -1
		}

		for range absInt(move) {
			dial += tick
			if dial == 0 || dial == 100 {
				zeroes++
				dial = 0
			} else if dial == -1 {
				dial = 99
			}
		}
	}

	fmt.Println("zeroes:", zeroes)
}
