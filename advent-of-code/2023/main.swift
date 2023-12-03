//
//  Advent of Code 2023 ⭐️
//

import Foundation

let EXAMPLE = "/Users/kris/Documents/aoc23/example.txt"
let INPUT = "/Users/kris/Documents/aoc23/input.txt"


func day4() {
    var result = 0
    for line in readLines(filename: EXAMPLE) {
        print(line)
        result += 1
    }
    print(result)
}

day4()
