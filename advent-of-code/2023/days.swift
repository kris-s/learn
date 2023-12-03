//
//  days.swift
//  aoc23
//
//  Created by Kris Shamloo on 11/25/23.
//

import Foundation

let DIGITS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
let STRING_DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


func readLines(filename: String) -> [String] {
    let content: String
    do {
        content = try String(contentsOfFile: filename)
    } catch {
        print(error)
        abort()
    }
    
    var lines: [String] = []

    for line in content.split(separator: "\n") {
        lines.append(String(line))
    }

    return lines
}

struct Point: Hashable {
    var x: Int
    var y: Int
    var width: Int
    var height: Int

    func neighbors(width: Int, height: Int) -> [Point] {
        var n: [Point] = []

        let vertical = [-1, 0, 1]
        let horizontal = [-1, 0, 1]

        for dy in vertical {
            for dx in horizontal {
                if dy == 0 && dx == 0 { continue }
                let p = Point(x: x + dx, y: y + dy, width: width, height: height)
                if p.inBounds() {
                    n.append(p)
                }
            }
        }

        return n
    }

    func inBounds() -> Bool {
        if x < 0 {
            return false
        }

        if y < 0 {
            return false
        }

        if x >= width {
            return false
        }

        if y >= height {
            return false
        }

        return true
    }
}



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

    for line in readLines(filename: INPUT) {
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


func day2() {
    let path = INPUT

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

        total += table.values.reduce(1, *)

    }
    print(total)
}


func day3() {
    let digits = "1234567890"
    let gridLines = readLines(filename: INPUT)

    var grid: [[String]] = []
    for line in gridLines {
        var lineValues: [String] = []
        for v in line {
            lineValues.append(String(v))
        }
        grid.append(lineValues)
    }

    let height = grid.count
    let width = grid[0].count

    var scan = ""
    var pointsToCheck: [Point] = []
    var gearCandidates: [Point: [Int]] = [:]
    var gearRatios: [Int] = []
    var gearPoint: Point = Point(x: 0, y: 0, width: width, height: height)

    for (y, line) in grid.enumerated() {

        for (x, ch) in line.enumerated() {
            if digits.contains(ch) {
                scan += String(ch)
                pointsToCheck.append(Point(x: x, y: y, width: width, height: height))
            } else if !scan.isEmpty {
                var canAppend = false
                for p in pointsToCheck {
                    for n in p.neighbors(width: width, height: height) {
                        let value = grid[n.y][n.x]
                        if !digits.contains(value) && value == "*" {
                            gearPoint = Point(x: n.x, y: n.y, width: width, height: height)
                            canAppend = true
                        }
                    }
                }
                if canAppend {
                    let gearValue = Int(scan)!
                    if gearCandidates[gearPoint] != nil {
                        gearCandidates[gearPoint]!.append(gearValue)
                    } else {
                        gearCandidates[gearPoint] = [gearValue]
                    }
                }
                scan = ""
                pointsToCheck = []
                gearPoint = Point(x: 0, y: 0, width: width, height: height)
            }
        }

    }

    print(gearCandidates)
    for value in gearCandidates.values {
        if value.count == 2 {
            gearRatios.append(value[0] * value[1])
        }
    }
    print(gearRatios.reduce(0, +))
}
