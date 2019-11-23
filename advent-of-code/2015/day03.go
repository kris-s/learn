package main

import (
	"fmt"
	"log"
)

type Pos struct {
	x int
	y int
}

func main() {
	var input string
	if _, err := fmt.Scanf("%s", &input); err != nil {
		log.Fatal(err)
	}

	var santaPos Pos
	var robotPos Pos

	var grid = map[Pos]int{
		santaPos: 1,
	}

	for i, rune := range input {
		var pos Pos
		if i%2 == 0 {
			pos = santaPos
		} else {
			pos = robotPos
		}

		switch rune {
		case '^':
			pos.y++
		case 'v':
			pos.y--
		case '>':
			pos.x++
		case '<':
			pos.x--
		}

		_, ok := grid[pos]
		if !ok {
			grid[pos] = 1
		} else {
			grid[pos]++
		}

		if i%2 == 0 {
			santaPos = pos
		} else {
			robotPos = pos
		}
	}

	fmt.Println("Houses visited:", len(grid))
}
