//
//  Advent of Code 2023 ⭐️
//

import Foundation

let EXAMPLE = "/Users/kris/Documents/aoc23/example.txt"

func day2() {
    let path = "/Users/kris/Documents/aoc23/2.txt"

    var total = 0

    for line in readLines(filename: path) {
        if line.isEmpty {
            continue
        }

        var table: [String: Int] = [
            "r": 0,
            "g": 0,
            "b": 0,
        ]

        let components = line.split(separator: " ")

        for (i, c) in components.enumerated() {
            if let value = Int(c) {
                if let maxSeen = table[String(components[i+1].first!)] {
                    if value > maxSeen {
                        table[String(components[i+1].first!)] = value
                    }
                }
            }
        }

        var power = 1
        for v in table.values {
            power *= v
        }
        total += power

    }
    print(total)
}

day2()
