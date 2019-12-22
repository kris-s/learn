package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

type OrbitalPair struct {
	orbiter string
	center  string
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

	orbits := []OrbitalPair{}
	for _, line := range lines {
		pair := strings.Split(line, ")")
		orbits = append(orbits, OrbitalPair{pair[1], pair[0]})
	}

	orbitalMap := make(map[string][]string)
	for _, op := range orbits {
		orbitalMap[op.orbiter] = ascendToCOM(orbits, op.center)
	}

	total := 0
	for _, value := range orbitalMap {
		total += len(value)
	}

	transfers := minTransfers(orbitalMap)

	fmt.Println("Part One:", total)
	fmt.Println("Part Two:", transfers)
}

func ascendToCOM(orbits []OrbitalPair, direct string) []string {
	ascent := []string{direct}

	for direct != "COM" {
		direct = nextUp(orbits, direct)
		ascent = append(ascent, direct)
	}

	return ascent
}

func nextUp(orbits []OrbitalPair, direct string) string {
	for _, op := range orbits {
		if op.orbiter == direct {
			return op.center
		}
	}

	return ""
}

func minTransfers(orbits map[string][]string) int {
	mine := orbits["YOU"]
	santas := orbits["SAN"]

	for i, myParent := range mine {
		for j, santaParent := range santas {
			if myParent == santaParent {
				return i + j
			}
		}
	}

	return 0
}
