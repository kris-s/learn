//
//  Advent of Code 2023 ⭐️
//

import Foundation

let EXAMPLE = "/Users/kris/Documents/aoc23/input.example"
let DAY1 = "/Users/kris/Documents/aoc23/1.txt"


func day1() {
    let digits: Set<Character> = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    let digitsSpelled: [String:String] = [
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    ]
    var calibration = 0

    for line in readLines(filename: DAY1) {
        if line.isEmpty {
            continue
        }
        
        var first = ""
        var last = ""
        var scan = ""
        
        for ch in line {
            guard first.isEmpty else { break }
            scan += String(ch)
            if digits.contains(ch) {
                first = String(ch)
                break
            }
            for key in digitsSpelled.keys {
                if scan.contains(key) {
                    first = digitsSpelled[key]!
                    break
                }
            }
        }
        
        scan = ""
        for ch in line.reversed() {
            guard last.isEmpty else { break }
            
            scan = "\(ch)\(scan)"
            if digits.contains(ch) {
                last = String(ch)
            }
            for key in digitsSpelled.keys {
                if scan.contains(key) {
                    last = digitsSpelled[key]!
                }
            }
        }

        let value = Int("\(first)\(last)") ?? 0
        print("\(line) adding", "\(value)")
        calibration += value
        print("----")
    }
    print(calibration)
}

day1()
