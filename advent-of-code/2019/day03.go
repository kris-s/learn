package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type Point struct {
	X int
	Y int
}

func main() {
	lines := []string{}
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	wire1 := wirePoints(strings.Split(lines[0], ","))
	wire2 := wirePoints(strings.Split(lines[1], ","))

	intersections := findIntersections(wire1, wire2)
	fmt.Println("Part One:", minPoint(intersections).Manhattan())
	fmt.Println("Part Two:", walkBack(intersections[1], wire1, wire2))
}

func wirePoints(instructions []string) []Point {
	points := []Point{Point{X: 0, Y: 0}}

	for _, inst := range instructions {
		lastPoint := points[len(points)-1]

		dir := inst[0]
		val, err := strconv.Atoi(inst[1:])
		if err != nil {
			log.Fatal(err)
		}

		switch dir {
		case 'U':
			for segment := 1; segment < val+1; segment++ {
				p := Point{X: lastPoint.X, Y: lastPoint.Y + segment}
				points = append(points, p)
			}
		case 'R':
			for segment := 1; segment < val+1; segment++ {
				p := Point{X: lastPoint.X + segment, Y: lastPoint.Y}
				points = append(points, p)
			}
		case 'D':
			for segment := 1; segment < val+1; segment++ {
				p := Point{X: lastPoint.X, Y: lastPoint.Y - segment}
				points = append(points, p)
			}
		case 'L':
			for segment := 1; segment < val+1; segment++ {
				p := Point{X: lastPoint.X - segment, Y: lastPoint.Y}
				points = append(points, p)
			}
		default:
			log.Fatalf("Unknown instruction: %s\n", inst)
		}
	}

	return points
}

func (p Point) Manhattan() int {
	distance := 0
	if p.X < 0 {
		distance += -p.X
	} else {
		distance += p.X
	}

	if p.Y < 0 {
		distance += -p.Y
	} else {
		distance += p.X
	}

	return distance
}

func findIntersections(p1, p2 []Point) []Point {
	intersections := []Point{}

	for _, point := range p1 {
		if containsPoint(p2, point) {
			intersections = append(intersections, point)
		}
	}
	return intersections
}

func containsPoint(points []Point, point Point) bool {
	for _, p := range points {
		if p == point {
			return true
		}
	}
	return false
}

func minPoint(points []Point) Point {
	minPoint := Point{X: 1e10, Y: 1e10}
	minDistance := minPoint.Manhattan()

	for _, p := range points {
		if p.X == 0 && p.Y == 0 {
			continue
		}
		distance := p.Manhattan()
		if distance < minDistance {
			minDistance = distance
			minPoint = p
		}
	}
	return minPoint
}

func walkBack(p Point, wire1, wire2 []Point) int {
	count := 0
	for i, point := range wire1 {
		if point == p {
			count += i
			break
		}
	}
	for i, point := range wire2 {
		if point == p {
			count += i
			break
		}
	}
	return count
}
