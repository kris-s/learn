//
//  Advent of Code 2023 ⭐️
//

import Foundation

let EXAMPLE = "/Users/kris/Documents/aoc23/example.txt"
let INPUT = "/Users/kris/Documents/aoc23/input.txt"

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

//    print("seeds:", seeds)

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
    for (i, seed) in seeds.enumerated() {
        let location = seedMapper(maps: maps, value: seed)
        if location < minLocation {
            minLocation = location
        }
    }
    print(minLocation)
}

day5()
