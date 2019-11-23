package main

import (
	"fmt"
	"log"
	"strings"
)

func main() {
	distances := make(map[string]int)
	locations := []string{}
	for {
		var a, b string
		var dist int
		if _, err := fmt.Scanf("%s to %s = %d", &a, &b, &dist); err != nil {
			break
		}
		locations = append(locations, a)
		locations = append(locations, b)
		key := fmt.Sprintf("%s to %s", a, b)
		distances[key] = dist
	}

	locations = removeDuplicates(locations)
	routes := getRoutes(locations)

	shortest := totalDistance(routes[0], distances)
	longest := 0

	for _, r := range routes {
		total := totalDistance(r, distances)
		if total < shortest {
			shortest = total
		} else if total > longest {
			longest = total
		}
		fmt.Println(strings.Join(r, " -> "), "=", total)
	}

	fmt.Println("Shortest route:", shortest)
	fmt.Println(" Longest route:", longest)
}

func removeDuplicates(dupes []string) []string {
	locations := make(map[string]struct{})

	for _, d := range dupes {
		if _, ok := locations[d]; !ok {
			locations[d] = struct{}{}
		}
	}

	locs := []string{}
	for key := range locations {
		locs = append(locs, key)
	}

	return locs
}

func getRoutes(locations []string) [][]string {
	routes := [][]string{}
	// Heap's algorithm to generate permutations
	var helper func(locs []string, n int)
	helper = func(locs []string, n int) {
		if n == 1 {
			tmp := make([]string, len(locs))
			copy(tmp, locs)
			routes = append(routes, tmp)
		} else {
			for i := 0; i < n; i++ {
				helper(locs, n-1)
				if n%2 == 1 {
					tmp := locs[i]
					locs[i] = locs[n-1]
					locs[n-1] = tmp
				} else {
					tmp := locs[0]
					locs[0] = locs[n-1]
					locs[n-1] = tmp
				}
			}
		}
	}
	helper(locations, len(locations))
	return routes
}

func totalDistance(route []string, distances map[string]int) int {
	total := 0
	n := len(route) - 1
	for i := 0; i < n; i++ {
		key1 := fmt.Sprintf("%s to %s", route[i], route[i+1])
		key2 := fmt.Sprintf("%s to %s", route[i+1], route[i])

		d, ok := distances[key1]
		if ok {
			total += d
			continue
		}
		d, ok = distances[key2]
		if ok {
			total += d
			continue
		} else {
			log.Fatalf("Error checking distance for %s/%s", key1, key2)
		}
	}

	return total
}
