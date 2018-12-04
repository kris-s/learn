// Advent of Code 2018
package main

import (
	"fmt"
	"strconv"
	"strings"
)

func main() {
	fmt.Println("It's time to save Christmas. 🎄")

	// fmt.Println(dayOneA(dayOneInput))
	// fmt.Println(dayOneB(dayOneInput))

	// fmt.Println(dayTwoA(dayTwoInput))
	// fmt.Println(dayTwoB(dayTwoInput))

	fmt.Println(dayThree(dayThreeInput))
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
