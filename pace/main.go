// pace takes a given run and outputs your average pace
package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: pace 5mi 41m29s")
		return
	}

	distance, err := parseDistance(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	duration, err := time.ParseDuration(os.Args[2])
	if err != nil {
		log.Fatal(err)
	}

	durationNs := float64(duration.Nanoseconds())

	kmPace := time.Duration(durationNs / distance).String()
	miPace := time.Duration(durationNs / kmToMiles(distance)).String()

	fmt.Printf("\nKm:	%.2f	%s per kilometer\n", distance, kmPace)
	fmt.Printf("Miles:	%.2f	%s per mile\n\n", kmToMiles(distance), miPace)
}

func parseDistance(s string) (float64, error) {
	// miles
	if strings.HasSuffix(s, "mi") ||
		(strings.HasSuffix(s, "m") && !strings.HasSuffix(s, "km")) {
		stringValue := strings.Split(s, "m")[0]
		miles, err := strconv.ParseFloat(stringValue, 64)
		if err != nil {
			return 0.0, err
		}
		return milesToKm(miles), nil
	}

	// kilometers
	stringValue := strings.Split(s, "k")[0]
	return strconv.ParseFloat(stringValue, 64)

}

func milesToKm(miles float64) float64 {
	return miles * 1.60934
}

func kmToMiles(km float64) float64 {
	return km / 1.60934
}
