// Advent of Code 2018
package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

func main() {
	fmt.Println("It's time to save Christmas. 🎄")

	daySix(daySixInput)
	// dayFive(dayFiveInput)
	// dayFour(dayFourInput)
	// fmt.Println(dayThree(dayThreeInput))
	// fmt.Println(dayTwoA(dayTwoInput))
	// fmt.Println(dayTwoB(dayTwoInput))
	// fmt.Println(dayOneA(dayOneInput))
	// fmt.Println(dayOneB(dayOneInput))
}

func daySix(input string) {
	type Point struct {
		x, y int
		name string
	}

	points := []Point{}
	grid := [500][500]string{}

	for y, row := range grid {
		for x, _ := range row {
			grid[y][x] = "."
		}
	}

	for i, p := range strings.Split(input, "\n") {
		point := Point{}
		fmt.Sscanf(p, "%d, %d", &point.x, &point.y)
		point.name = fmt.Sprintf("p%d", i)
		points = append(points, point)
		grid[point.y][point.x] = point.name

	}

	abs := func(n int) int {
		if n < 0 {
			return -n
		}
		return n
	}

	sum := func(nums []int) int {
		total := 0
		for _, n := range nums {
			total += n
		}
		return total
	}

	manhattanDistance := func(a, b Point) int {
		return abs(a.x-b.x) + abs(a.y-b.y)
	}

	pointOwner := func(points []Point, point Point) string {
		distances := make(map[Point]int)
		for _, p := range points {
			distances[p] = manhattanDistance(p, point)
		}

		min := 100000
		owner := ""
		for k, v := range distances {
			if v < min {
				min = v
				owner = k.name
			}
		}

		for k, v := range distances {
			if k.name == owner {
				continue
			}

			if v == min {
				owner = ".."
			}
		}
		return owner
	}

	for y, row := range grid {
		for x, _ := range row {
			grid[y][x] = strings.ToLower(pointOwner(points, Point{x, y, ""}))
		}
	}

	scores := make(map[string]int)
	for y, row := range grid {
		for x, _ := range row {
			if x == 0 || y == 0 || x == len(row)-1 || y == len(grid)-1 {
				scores[grid[y][x]] = -1
			} else if scores[grid[y][x]] < 0 {
				continue
			} else {
				scores[grid[y][x]]++
			}
		}
	}

	max := 0
	winner := ""
	for k, v := range scores {
		if v > max {
			max = v
			winner = k
		}
	}

	fmt.Println("Part 1:", winner, max)

	regionSize := 0
	for y, row := range grid {
		for x, _ := range row {
			distances := []int{}
			point := Point{x, y, ""}
			for _, p := range points {
				distances = append(distances, manhattanDistance(p, point))
			}
			if sum(distances) < 10000 {
				regionSize++
			}

		}
	}

	fmt.Println("Part 2:", regionSize)
}

func dayFive(input string) {
	polymer := []byte(input)

	react := func(polymer []byte) int {
		i := 0

		for i < len(polymer)-2 {

			var diff byte

			if polymer[i] > polymer[i+1] {
				diff = polymer[i] - polymer[i+1]
			} else {
				diff = polymer[i+1] - polymer[i]
			}

			if diff == 32 {
				if i+2 < len(polymer) {
					polymer = append(polymer[:i], polymer[i+2:]...)
				} else {
					polymer = polymer[:i]
				}
				if i > 0 {
					i--
				}
			} else {
				i++
			}
		}
		return len(polymer)
	}

	fmt.Println("Part 1:", react(polymer))

	table := make(map[string]int)

	// A = 65
	alphabet := []string{
		"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
		"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}
	for _, letter := range alphabet {
		reduced := strings.Replace(input, letter, "", -1)
		reduced = strings.Replace(reduced, strings.ToLower(letter), "", -1)
		reducedPolymer := []byte(reduced)
		table[letter] = react(reducedPolymer)
	}

	min := 10000
	best := ""
	for k, v := range table {
		if v < min {
			min = v
			best = k
		}
	}
	fmt.Println("Part 2:", best, min)
}

func dayFour(input string) {
	logs := strings.Split(input, "\n")
	sort.Strings(logs)

	guardHabits := make(map[string][60]int)
	currentGuard := ""
	start := 0
	end := 0

	for _, log := range logs {

		if strings.Contains(log, "Guard") {
			currentGuard = strings.Split(log, "]")[1]
			start = 0
			end = 0

			_, ok := guardHabits[currentGuard]
			if !ok {
				guardHabits[currentGuard] = [60]int{}
			}
		} else if strings.Contains(log, "falls asleep") {
			startS := strings.Split(log, ":")[1]
			startS = strings.Split(startS, "]")[0]
			start, _ = strconv.Atoi(startS)
		} else if strings.Contains(log, "wakes up") {
			endS := strings.Split(log, ":")[1]
			endS = strings.Split(endS, "]")[0]
			end, _ = strconv.Atoi(endS)

			for j := start; j < end; j++ {
				habits := guardHabits[currentGuard]
				habits[j]++
				guardHabits[currentGuard] = habits
			}
		}
	}

	sleepiestGuard := ""
	sleepiestMinute := 0
	max := 0

	sumInts := func(ints [60]int) int {
		total := 0
		for _, v := range ints {
			total += v
		}
		return total
	}

	for k, v := range guardHabits {
		total := sumInts(v)
		if total > max {
			max = total
			sleepiestGuard = k
		}
	}

	max = 0
	sleepTimes := guardHabits[sleepiestGuard]
	for i, m := range sleepTimes {
		if m > max {
			max = m
			sleepiestMinute = i
		}
	}

	sleepiestGuard = strings.Split(sleepiestGuard, "#")[1]
	sleepiestGuard = strings.Split(sleepiestGuard, " begins")[0]
	guardId, _ := strconv.Atoi(sleepiestGuard)

	fmt.Println("Strategy 1:", guardId*sleepiestMinute)

	max = 0
	for k, v := range guardHabits {
		for i, m := range v {
			if m > max {
				max = m
				sleepiestMinute = i
				sleepiestGuard = k
			}
		}
	}

	sleepiestGuard = strings.Split(sleepiestGuard, "#")[1]
	sleepiestGuard = strings.Split(sleepiestGuard, " begins")[0]
	guardId, _ = strconv.Atoi(sleepiestGuard)

	fmt.Println("Strategy 2:", guardId*sleepiestMinute)

}

func dayThree(input string) (int, string) {
	type Claim struct {
		Id                       string
		Left, Right, Top, Bottom int
	}

	maxRight, maxDown := 0, 0
	claims := []Claim{}

	for _, sc := range strings.Split(input, "--") {
		c := Claim{}
		_, _ = fmt.Sscanf(sc, "#%s @ %d,%d: %dx%d", &c.Id, &c.Left, &c.Top, &c.Right, &c.Bottom)
		c.Right += c.Left
		c.Bottom += c.Top

		if c.Right > maxRight {
			maxRight = c.Right
		}

		if c.Bottom > maxDown {
			maxDown = c.Bottom
		}

		claims = append(claims, c)
	}

	overlaps := 0
	fabric := [][]int{}
	for i := 0; i < maxDown; i++ {
		row := []int{}
		for j := 0; j < maxRight; j++ {
			count := 0
			for _, claim := range claims {
				if claim.Top <= i && i < claim.Bottom && claim.Left <= j && j < claim.Right {
					count++
				}
			}
			if count > 1 {
				overlaps++
			}
			row = append(row, count)
		}
		fabric = append(fabric, row)
	}

	claimsOverlap := func(c1, c2 Claim) bool {
		clearVert := false
		clearHoriz := false

		if c1.Top > c2.Top {
			clearVert = c1.Top >= c2.Bottom
		} else {
			clearVert = c1.Bottom <= c2.Top
		}

		if c1.Left < c2.Left {
			clearHoriz = c1.Right <= c2.Left
		} else {
			clearHoriz = c1.Left >= c2.Right
		}
		return !(clearHoriz || clearVert)
	}

	clean := ""
	for i, c1 := range claims {
		checked := 0
		for j, c2 := range claims {
			checked++
			if i == j {
				continue
			}

			if claimsOverlap(c1, c2) {
				break
			}

			if checked+1 == len(claims) {
				clean = c1.Id
				break
			}
		}
	}

	return overlaps, clean
}

func dayTwoA(input string) int {
	twos := 0
	threes := 0

	for _, val := range strings.Split(input, ",") {
		counts := make(map[rune]int)

		for _, r := range val {
			counts[r] = 0
		}
		for _, r := range val {
			counts[r] += 1
		}

		incTwos := false
		incThrees := false
		for _, v := range counts {
			if v == 2 {
				incTwos = true
			}
			if v == 3 {
				incThrees = true
			}
		}

		if incTwos {
			twos++
		}
		if incThrees {
			threes++
		}
	}

	return twos * threes
}

func dayTwoB(input string) string {
	inputs := strings.Split(input, ",")
	var matches [2]string

	for i, id1 := range inputs {
		for j, id2 := range inputs {
			if i == j {
				continue
			}

			variance := 0

			for k, _ := range id1 {
				if id1[k] != id2[k] {
					variance++

					if variance > 1 {
						break
					}
				}
			}

			if variance == 1 {
				matches[0] = id1
				matches[1] = id2
				break
			} else {
				continue
			}
		}
	}

	match := ""
	for i, _ := range matches[0] {
		if matches[0][i] == matches[1][i] {
			match = match + string(matches[0][i])
		}
	}
	return match
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
