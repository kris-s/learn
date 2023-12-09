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

func readAsGrid(filename: String) -> [Point] {
    var points: [Point] = []

    let lines = readLines(filename: filename)
    let height = lines.count
    let width = lines[0].count

    for (y, line) in lines.enumerated() {
        for (x, ch) in line.enumerated() {
            points.append(Point(
                x: x,
                y: y,
                width: width,
                height: height,
                value: String(ch)))
        }
    }

    return points
}

struct Point: Hashable {
    var x: Int
    var y: Int
    var width: Int
    var height: Int
    var value: String = ""

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

func singleSeedMapper(rules: [(Int, Int, Int)], value: Int) -> Int {
    for rule in rules {
        let (dest, source, length) = rule
        let offset = source - dest
        if value >= source && value <= source+length {
            return value - offset
        }
    }

    return value
}

func seedMapper(maps: [[(Int, Int, Int)]], value: Int) -> Int {
    var result = value
    for map in maps {
        result = singleSeedMapper(rules: map, value: result)
    }

    return result
}

func rawToRules(raw: [String]) -> [(Int, Int, Int)] {
    var values: [(Int, Int, Int)] = []
    for rawLine in raw {
        let split = rawLine.split(separator: " ")
        let tuple: (Int, Int, Int) = (Int(split[0])!, Int(split[1])!, Int(split[2])!)
        values.append(tuple)
    }
    return values
}


func day5() {
    let lines = readLines(filename: INPUT)
    let seedData = lines[0].split(separator: " ").compactMap({ Int($0) } )
    var seeds: [Int] = []

    for (i, value) in seedData.enumerated() {
        if i % 2 == 0 { continue }
        let seed = seedData[i-1]
        let range = value

        for i in 0..<value {
            seeds.append(seed + i)
        }
        print("seed", seed, "range", range)
    }

    var maps: [[(Int, Int, Int)]] = []
    var currentMap: [String] = []

    for line in lines[2...] {
        if line.contains("map:") {
            maps.append(rawToRules(raw: currentMap))
            currentMap = []
        } else if !line.isEmpty {
            currentMap.append(line)
        }
    }

    maps.append(rawToRules(raw: currentMap))
    print("maps:", maps)

    var minLocation: Int = Int.max
    for seed in seeds {
        let location = seedMapper(maps: maps, value: seed)
        if location < minLocation {
            minLocation = location
        }
    }
    print(minLocation)
}

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

let face: [String: Int] = [
    "T": 10,
    "J": 1,
    "Q": 12,
    "K": 13,
    "A": 14,
]

enum HandType: Int {
    case five = 7
    case four = 6
    case fh = 5
    case three = 4
    case twopair = 3
    case pair = 2
    case high = 1
}

struct Hand {
    var raw: String
    var values: [Int]
    var bid: Int
    var type: HandType

    init(raw: String, bid: Int) {
        self.values = []
        self.raw = raw
        self.bid = bid

        var jokers = 0

        for ch in raw {
            if ch == "J" {
                jokers += 1
            }
            if let v = Int(String(ch)) {
                self.values.append(v)
            } else {
                self.values.append(face[String(ch)]!)
            }
        }

        let counts = self.values.reduce(into: [:]) { $0[$1, default: 0] += 1 }

        if counts.values.contains(5) {
            self.type = .five
        } else if counts.values.contains(4) {
            self.type = .four
        } else if counts.values.contains(3) && counts.values.contains(2) {
            self.type = .fh
        } else if counts.values.contains(3) {
            self.type = .three
        } else if counts.values.contains(2) && counts.count == 3 {
            self.type = .twopair
        } else if counts.values.contains(2) {
            self.type = .pair
        } else {
            self.type = .high
        }

        guard jokers > 0 else { return }
        guard self.type != .five else { return }

        if jokers > 3 {
            // JJJJ2
            // JJJJJ
            self.type = .five
            return
        }

        if self.type == .four {
            // AAAAJ
            self.type = .five
            return
        }

        if self.type == .fh {
            // AAAJJ or JJJAA
            self.type = .five
            return
        }

        if self.type == .three && jokers == 1 {
            // AAA2J
            self.type = .four
            return
        }

        if self.type == .three && jokers == 3 {
            // JJJ23
            self.type = .four
            return
        }

        if self.type == .twopair && jokers == 1 {
            // AA22J
            self.type = .fh
            return
        }

        if self.type == .twopair && jokers > 1 {
            // AAJJ4
            self.type = .four
            return
        }

        if self.type == .pair {
            // AA23J
            // JJ234
            self.type = .three
            return
        }

        if self.type == .high {
            // J2345
            self.type = .pair
            return
        }


    }
}

func compareHand(lhs: Hand, rhs: Hand) -> Bool {
    print("compare", lhs.raw, rhs.raw)
    if lhs.type != rhs.type {
        return lhs.type.rawValue > rhs.type.rawValue
    }

    for (i, val) in lhs.values.enumerated() {
        if val == rhs.values[i] { continue }
        if val > rhs.values[i] {
            return true
        } else {
            return false
        }
    }
    return false
}

func day7() {
    let lines = readLines(filename: INPUT)
    var result = 0

    var hands: [Hand] = []

    for line in lines {
        let values = line.split(separator: " ")
        let hand = Hand(raw: String(values[0]), bid: Int(values[1])!)
        hands.append(hand)
    }

    hands.sort(by: { compareHand(lhs: $0, rhs: $1)})
    print(hands)

    for (i, hand) in hands.enumerated() {
        let rank = hands.count - i
        print(hand.raw, rank, hand.bid, rank * hand.bid)
        result += rank * hand.bid
    }

    print(result)
}


struct Node {
    var value: String
    var left: String
    var right: String
}

func day8() {
    let lines = readLines(filename: EXAMPLE)

    var steps: [String] = []
    for ch in lines[0] {
        steps.append(String(ch))
    }

    var ghostNodes: [String] = []
    var nodes: [String:Node] = [:]

    for line in lines[1...] {
        let values = line.split(separator: " ")
        let name = String(values[0])

        if name.last == "A" {
            ghostNodes.append(name)
        }

        var left = values[2]
        left.removeFirst()
        left.removeLast()

        var right = values[3]
        right.removeLast()
        print(name, left, right)
        nodes[name] = Node(value: name, left: String(left), right: String(right))
    }

    print(ghostNodes)

    var stepCount = 1
    var index = 0

    var stepsToZ: [Int: [Int]] = [:]
    for (i, _) in ghostNodes.enumerated() {
        stepsToZ[i] = []
    }

    while true {
        // advance all ghost nodes
        for (i, current) in ghostNodes.enumerated() {
            let go = steps[index % steps.count]
            let nextNode = nodes[current]!

            if go == "L" {
                ghostNodes[i] = nextNode.left
            } else {
                ghostNodes[i] = nextNode.right
            }

            if ghostNodes[i].last == "Z" {
                stepsToZ[i]?.append(stepCount)
            }
        }

        // check all ghost nodes
        if ghostNodes.allSatisfy({ $0.last == "Z" }){
            break
        }

        if stepCount % 1000000 == 0 {
            print("\(stepCount) - \(ghostNodes)")
            print(stepsToZ)

            var minimums: [Int] = []
            for factors in stepsToZ.values {
                let sortedFactors = factors.sorted()
                minimums.append(sortedFactors[0])
            }

            // lcm was done with python's math.lcm because I am lazy
            print("mins:", minimums)
        }
        stepCount += 1
        index += 1

    }
    print(stepCount)
}
