//
//  Advent of Code 2023 ⭐️
//

import Foundation

let EXAMPLE = "/Users/kris/Documents/aoc23/example.txt"
let INPUT = "/Users/kris/Documents/aoc23/input.txt"


func day6() {

    var result = 1

    // input
    let times: [Int] = [47707566]
    let distances: [Int] = [282107911471062]

    for (raceIndex, time) in times.enumerated() {
        var waysToWin = 0

        for holdTime in 1..<time {
            let speed = holdTime
            let timeLeft = time - holdTime
            let distance = timeLeft * speed

            if distance > distances[raceIndex] {
                waysToWin += 1
            }
        }
        result *= waysToWin
        waysToWin = 0
    }

    print(result)
}

day6()
