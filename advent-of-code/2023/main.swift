//
//  Advent of Code 2023 ⭐️
//

import Foundation

let EXAMPLE = "/Users/kris/Documents/aoc23/example.txt"
let INPUT = "/Users/kris/Documents/aoc23/input.txt"

func cardMatches(line: String) -> Int {
    let s1 = line.split(separator: ": ")
    let s2 = s1[1].split(separator: "|")

    let winning = s2[0].split(separator: " ").compactMap({ Int($0) })
    let have = s2[1].split(separator: " ").compactMap({ Int($0) })

    let winningSet = Set<Int>(winning)
    let haveSet = Set<Int>(have)

    return winningSet.intersection(haveSet).count
}

func day4() {
    let lines = readLines(filename: INPUT)

    var cardCopies: [Int: Int] = [:]
    var knownMatchCounts: [Int: Int] = [:]
    var copiesToProcess: [Int] = []

    for (i, line) in lines.enumerated() {
        cardCopies[i+1] = 1

        let matches = cardMatches(line: line)
        knownMatchCounts[i+1] = matches
        if matches > 0 {
            for offset in 1...matches {
                copiesToProcess.append(i+offset)
            }
        }
    }

    while !copiesToProcess.isEmpty {
        let index = copiesToProcess.popLast()!
        cardCopies[index+1]! += 1
        let matches = knownMatchCounts[index+1]!
        if matches > 0 {
            for offset in 1...matches {
                copiesToProcess.append(index+offset)
            }
        }
    }

    print(cardCopies)
    print(cardCopies.values.reduce(0, +))
}

day4()
