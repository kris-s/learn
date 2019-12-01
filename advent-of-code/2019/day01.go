package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
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

	nums := convert(lines)
	fmt.Println("Day one:", sumRocket(nums, rocket1))
	fmt.Println("Day two:", sumRocket(nums, rocket2))
}

func convert(lines []string) []int {
	nums := []int{}
	for _, l := range lines {
		value, err := strconv.Atoi(l)
		if err != nil {
			log.Fatal(err)
		}
		nums = append(nums, value)
	}
	return nums
}

func sumRocket(nums []int, eq func(int) int) int {
	count := 0
	for i := range nums {
		count += eq(nums[i])
	}
	return count
}

func rocket1(value int) int {
	value /= 3
	value -= 2
	return value
}

func rocket2(value int) int {
	total := rocket1(value)
	temp := total
	for temp > 0 {
		temp = rocket1(temp)
		if temp > 0 {
			total += temp
		}
	}
	return total
}
