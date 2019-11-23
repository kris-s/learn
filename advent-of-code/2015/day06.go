package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

const on = "on"
const off = "off"
const toggle = "toggle"

type Instruction struct {
	a, b, x, y int
	command    string
}

func main() {
	var lights [1000][1000]int

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}

		var i Instruction
		if strings.HasPrefix(line, "turn on ") {
			line = strings.TrimPrefix(line, "turn on ")
			i.command = on
		} else if strings.HasPrefix(line, "turn off ") {
			line = strings.TrimPrefix(line, "turn off ")
			i.command = off
		} else if strings.HasPrefix(line, "toggle ") {
			line = strings.TrimPrefix(line, "toggle ")
			i.command = toggle
		} else {
			log.Fatal("Unknown command ", line)
		}

		_, err := fmt.Sscanf(line, "%d,%d through %d,%d", &i.a, &i.b, &i.x, &i.y)
		if err != nil {
			log.Fatal(err)
		}

		lights = parseInstruction(i, lights)
	}

	count := 0
	for i, row := range lights {
		for j := range row {
			count += lights[i][j]
		}
	}
	fmt.Println("Total brightness:", count)
}

func parseInstruction(inst Instruction, lights [1000][1000]int) [1000][1000]int {
	for i, row := range lights {
		if i < inst.a || i > inst.x {
			continue
		}
		for j, brightness := range row {
			if j < inst.b || j > inst.y {
				continue
			}
			switch inst.command {
			case on:
				lights[i][j] = brightness + 1
			case toggle:
				lights[i][j] = brightness + 2
			case off:
				if brightness > 0 {
					lights[i][j] = brightness - 1
				}
			}
		}
	}
	return lights
}
