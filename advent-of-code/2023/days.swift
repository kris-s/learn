//
//  days.swift
//  aoc23
//
//  Created by Kris Shamloo on 11/25/23.
//

import Foundation

func readLines(filename: String) -> [Substring] {
    let content: String
    do {
        content = try String(contentsOfFile: filename)
    } catch {
        print(error)
        abort()
    }
    
    return content.split(separator: "\n")
}
