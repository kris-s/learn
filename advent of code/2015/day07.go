package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type LineInfo struct {
	line     string
	name     string
	inst     string
	a        string
	b        string
	resolved bool
}

func main() {
	var circuit = make(map[string]uint16)
	var lines []LineInfo

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}
		lines = append(lines, parseLineInfo(line))
	}

	circuit = resolveCircuit(lines, circuit)
	fmt.Println("Part one:", circuit["a"])

	// part 2
	circuit["b"] = circuit["a"]
	for key := range circuit {
		if key != "b" {
			delete(circuit, key)
		}
	}
	for i := range lines {
		if lines[i].name != "b" {
			lines[i].resolved = false
		}
	}

	circuit = resolveCircuit(lines, circuit)
	fmt.Println("Part two:", circuit["a"])

}

func parseLineInfo(line string) LineInfo {
	lineInfo := LineInfo{}
	lineSplit := strings.Split(line, " -> ")
	lineInfo.name = lineSplit[1]

	splitInst := strings.Split(lineSplit[0], " ")
	if len(splitInst) == 1 {
		// 44430 -> b
		lineInfo.inst = "READ"
		lineInfo.a = splitInst[0]
	} else if len(splitInst) == 2 {
		// NOT gs -> gt
		lineInfo.inst = "NOT"
		lineInfo.a = splitInst[1]
	} else {
		// dd OR do -> dp
		lineInfo.inst = splitInst[1]
		lineInfo.a = splitInst[0]
		lineInfo.b = splitInst[2]
	}
	return lineInfo
}

func resolveCircuit(lines []LineInfo, circuit map[string]uint16) map[string]uint16 {
	loopCount := 0
	for anyUnresolved(lines) {
		loopCount++
		for i := range lines {
			if lines[i].resolved {
				continue
			}
			value, err := parseInstruction(lines[i], circuit)
			if err != nil {
				continue
			} else {
				circuit[lines[i].name] = value
				lines[i].resolved = true
			}
		}
	}
	return circuit
}

func anyUnresolved(lines []LineInfo) bool {
	for i := range lines {
		if !lines[i].resolved {
			return true
		}
	}
	return false
}

func castOrReadCircuit(name string, circuit map[string]uint16) (uint16, error) {
	// try to cast
	if value, err := strconv.Atoi(name); err == nil {
		return uint16(value), nil
	}
	// try to read the circuit
	value, ok := circuit[name]
	if ok {
		return value, nil
	}
	return 0, fmt.Errorf("check-again %s", name)
}

func parseInstruction(li LineInfo, circuit map[string]uint16) (uint16, error) {
	var a, b uint16
	var err error
	if li.inst == "READ" || li.inst == "NOT" {
		a, err = castOrReadCircuit(li.a, circuit)
		if err != nil {
			return 0, err
		}
	} else {
		a, err = castOrReadCircuit(li.a, circuit)
		if err != nil {
			return 0, err
		}
		b, err = castOrReadCircuit(li.b, circuit)
		if err != nil {
			return 0, err
		}
	}

	switch li.inst {
	case "READ":
		return a, nil
	case "NOT":
		return ^a, nil
	case "AND":
		return a & b, nil
	case "OR":
		return a | b, nil
	case "LSHIFT":
		return a << b, nil
	case "RSHIFT":
		return a >> b, nil
	}
	return 0, fmt.Errorf("unexpectedly fell through")
}
