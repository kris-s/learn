package main

import (
	"fmt"
	"math/rand"
	"time"
)

type State struct {
	name          string
	probabilities []float64
}

func main() {
	chain := []State{
		State{name: "rain", probabilities: []float64{0.3, 0.3, 0.4}},
		State{name: "sun", probabilities: []float64{0.1, 0.8, 0.1}},
		State{name: "cloudy", probabilities: []float64{0.4, 0.1, 0.5}},
	}

	state := 0

	if err := validChain(chain); err == nil {
		for {
			state, err := update(chain, state)
			if err != nil {
				fmt.Println(err)
				break
			}
			fmt.Println(chain[state].name)
			time.Sleep(1000000000)
		}
	} else {
		fmt.Println(err)
	}
}

func validChain(chain []State) error {

	chainLength := len(chain)
	for _, s := range chain {
		// chain and probabilities must have equal lengths
		if chainLength != len(s.probabilities) {
			return fmt.Errorf(
				"Chain length not equal to probability length. \tState: %v", s)
		}
		// sum of a State's probabilities must equal 1.0
		if sum := calcSum(s.probabilities); sum != 1.0 {
			return fmt.Errorf("Probabilities don't sum to 1.0. \tState: %v", s)
		}

	}
	return nil
}

func update(chain []State, state int) (int, error) {
	p := chain[state].probabilities
	choice := rand.Float64()
	pSum := 0.0
	for i, p := range p {
		pSum += p
		if choice < pSum {
			return i, nil
		}
	}
	return 0, fmt.Errorf("There was an error altering states. \n\tChain: %v"+
		"\tChoice: %v", chain, choice)
}

func calcSum(s []float64) float64 {
	sum := 0.0
	for _, value := range s {
		sum += value
	}
	return sum
}
