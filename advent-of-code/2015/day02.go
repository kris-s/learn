package main

import (
	"fmt"
)

type Box struct {
	x int
	y int
	z int
}

func (b Box) surfaceArea() int {
	return (2 * b.x * b.y) + (2 * b.y * b.z) + (2 * b.z * b.x)
}

func (b Box) smallestSideArea() int {
	dims := []int{b.x * b.y, b.y * b.z, b.z * b.x}
	return minInt(dims)
}

func (b Box) smallestPerimeter() int {
	perims := []int{
		(b.x + b.x + b.y + b.y),
		(b.y + b.y + b.z + b.z),
		(b.z + b.z + b.x + b.x),
	}
	return minInt(perims)
}

func (b Box) volume() int {
	return b.x * b.y * b.z
}

func minInt(numbers []int) int {
	smallest := numbers[0]
	for _, num := range numbers {
		if num < smallest {
			smallest = num
		}
	}
	return smallest
}

func main() {
	paperTotal := 0
	ribbonTotal := 0
	for {
		var box Box
		if _, err := fmt.Scanf("%dx%dx%d", &box.x, &box.y, &box.z); err != nil {
			break
		}
		paperTotal += box.surfaceArea() + box.smallestSideArea()
		ribbonTotal += box.smallestPerimeter() + box.volume()
	}
	fmt.Println(" Paper needed:", paperTotal)
	fmt.Println("Ribbon needed:", ribbonTotal)
}
