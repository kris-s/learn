package main

import (
	"cmp"
	"embed"
	"flag"
	"fmt"
	"log"
	"slices"
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

func stringToDigits(raw string) []int {
	result := []int{}

	for _, ch := range raw {
		result = append(result, intOrPanic(string(ch)))
	}

	return result
}

func mergeRanges(a, b Range) (Range, bool) {
	if a.Lower <= b.Lower && a.Upper >= b.Lower-1 {
		if a.Upper > b.Upper {
			return Range{a.Lower, a.Upper}, true
		} else {
			return Range{a.Lower, b.Upper}, true
		}
	}

	if b.Lower <= a.Lower && b.Upper >= a.Lower-1 {
		if a.Upper > b.Upper {
			return Range{a.Lower, a.Upper}, true
		} else {
			return Range{a.Lower, b.Upper}, true
		}
	}

	return Range{}, false
}

func main() {
	flag.Parse()

	switch *dayChoice {
	case 1:
		day1("d1s.input", "d1i.input")
	case 2:
		day2("d2s.input", "d2i.input")
	case 3:
		day3("d3s.input", "d3i.input")
	case 4:
		day4("d4s.input", "d4i.input")
	case 5:
		day5("d5s.input", "d5i.input")
	default:
		fmt.Println("Invalid day choice:", *dayChoice)
	}
}

type Range struct {
	Lower, Upper int
}

type Point struct {
	X, Y int
}

type Grid struct {
	Width, Height int
	Points        []rune
}

func (g *Grid) ValueAt(x, y int) rune {
	return g.Points[y*g.Width+x]
}

func (g *Grid) SetAt(x, y int, value rune) {
	g.Points[y*g.Width+x] = value
}

func (g *Grid) Adjacents(x, y int) []Point {
	points := []Point{}

	// left side
	if x > 0 {
		// up
		if y > 0 {
			points = append(points, Point{x - 1, y - 1})
		}

		// middle
		points = append(points, Point{x - 1, y})

		// down
		if y < g.Height-1 {
			points = append(points, Point{x - 1, y + 1})
		}
	}

	// top middle
	if y > 0 {
		points = append(points, Point{x, y - 1})
	}

	// bottom middle
	if y < g.Height-1 {
		points = append(points, Point{x, y + 1})
	}

	// right side
	if x < g.Width-1 {
		// up
		if y > 0 {
			points = append(points, Point{x + 1, y - 1})
		}

		// middle
		points = append(points, Point{x + 1, y})

		// down
		if y < g.Height-1 {
			points = append(points, Point{x + 1, y + 1})
		}
	}

	return points
}

func day5(samplefile string, inputfile string) {
	// 3
	day5Fresh(samplefile)
	// 770
	day5Fresh(inputfile)
	// 14
	day5AllOptions(samplefile)
	// 357674099117260
	day5AllOptions(inputfile)
}

func day5AllOptions(filename string) {
	ranges, _ := day5RangesIds(filename)

	slices.SortFunc(ranges, func(a, b Range) int {
		return cmp.Compare(a.Lower, b.Lower)
	})

	count := 0

	for {
	RangeLoop:
		for i := range ranges {
			for j := range ranges {
				if i == j {
					continue
				}
				merged, ok := mergeRanges(ranges[i], ranges[j])

				if ok {
					ranges[i] = merged
					ranges = slices.Delete(ranges, j, j+1)
					slices.SortFunc(ranges, func(a, b Range) int {
						return cmp.Compare(a.Lower, b.Lower)
					})
					break RangeLoop
				}
			}
		}
		count++
		if count > 1000 {
			break
		}
	}

	total := 0
	for _, r := range ranges {
		total += r.Upper - r.Lower + 1
	}
	fmt.Println("part two:", total)
}

func day5Fresh(filename string) {
	ranges, ids := day5RangesIds(filename)

	freshIds := []int{}

TopLoop:
	for _, id := range ids {
		for _, r := range ranges {
			if id >= r.Lower && id <= r.Upper {
				freshIds = append(freshIds, id)
				continue TopLoop
			}
		}
	}

	fmt.Println("part one:", len(freshIds))
}

func day5RangesIds(filename string) ([]Range, []int) {
	input := getInput(filename)

	ranges := []Range{}
	ids := []int{}

	parseAsRange := true

	for _, line := range strings.Split(input, "\n") {
		if line == "" {
			parseAsRange = false
			continue
		}

		if parseAsRange {
			pair := strings.Split(line, "-")
			lower := intOrPanic(pair[0])
			upper := intOrPanic(pair[1])
			ranges = append(ranges, Range{lower, upper})
		} else {
			ids = append(ids, intOrPanic(line))
		}
	}

	return ranges, ids
}

func day4(samplefile string, inputfile string) {
	// 13
	day4Rolls(samplefile)
	// 1320
	day4Rolls(inputfile)
	// 43
	day4RollsSim(samplefile)
	// 8354
	day4RollsSim(inputfile)

}

func day4RollsSim(filename string) {
	grid := day4Grid(filename)

	total := 0

	for {
		accessible := day4Accessible(&grid)

		if len(accessible) == 0 {
			break
		}

		total += len(accessible)

		for _, p := range accessible {
			grid.SetAt(p.X, p.Y, '.')
		}
	}

	fmt.Println("part two:", total)
}

func day4Rolls(filename string) {
	grid := day4Grid(filename)

	accessible := day4Accessible(&grid)

	fmt.Println("part one:", len(accessible))
}

func day4Accessible(grid *Grid) []Point {
	accessible := []Point{}

	for x := range grid.Width {
		for y := range grid.Height {
			if grid.ValueAt(x, y) != '@' {
				continue
			}

			count := 0

			for _, p := range grid.Adjacents(x, y) {
				if grid.ValueAt(p.X, p.Y) == '@' {
					count++
				}
			}

			if count < 4 {
				accessible = append(accessible, Point{x, y})
			}
		}
	}

	return accessible
}

func day4Grid(filename string) Grid {
	input := getInput(filename)

	grid := Grid{}

	for y, row := range strings.Split(input, "\n") {
		if y == 0 {
			grid.Width = len(row)
		}
		grid.Height = y

		for _, value := range row {
			grid.Points = append(grid.Points, value)
		}
	}

	return grid
}

func day3(samplefile string, inputfile string) {
	// 357
	day3Joltage(samplefile)
	// 16927
	day3Joltage(inputfile)
	// 3121910778619
	day3BigJoltage(samplefile)
	// 167384358365132
	day3BigJoltage(inputfile)
}

func day3BigJoltage(filename string) {
	input := getInput(filename)

	joltages := []int{}

	for _, entry := range strings.Split(input, "\n") {
		batteries := stringToDigits(entry)
		if len(batteries) == 0 {
			continue
		}

		joltage := 0
		upper := 0
		lower := len(batteries) - 11
		scale := 100000000000

		for i := range 12 {
			choice := slices.Max(batteries[upper:lower])

			relativeIndex := slices.Index(batteries[upper:lower], choice)

			upper += relativeIndex + 1
			lower = len(batteries) - (11 - (i + 1))

			joltage += choice * scale
			scale /= 10
		}

		joltages = append(joltages, joltage)
	}

	fmt.Println("part two:", sumInts(joltages))
}

func day3Joltage(filename string) {
	input := getInput(filename)

	joltages := []int{}

	for _, entry := range strings.Split(input, "\n") {
		batteries := stringToDigits(entry)
		if len(batteries) == 0 {
			continue
		}

		first := slices.Max(batteries[0 : len(batteries)-1])
		firstIndex := slices.Index(batteries, first)
		second := slices.Max(batteries[firstIndex+1 : len(batteries)])

		joltages = append(joltages, first*10+second)
	}

	fmt.Println("part one:", sumInts(joltages))
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
