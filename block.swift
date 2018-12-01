#!/usr/bin/swift
import Foundation

let emoji: [String] = [
    "🐶",
    "🦁",
    "🐺",
    "🐉",
    "🐘",
    "🌺",
    "🍁",
    "🍦",
    "🍓",
    "🍏",
    "🚗",
    "⛵",
    "🦋",
    "🐳",
    "🌸",
    "⭐️",
    "🍎",
    "🚲",
    "⚔️",
    "🇺🇸",
    "🧛🏻‍♂️",
    "🧜🏻‍♀️",
    "🦑",
    "🦖",
    "🦕",
    "🐝",
]

let d = Date()
let choice = Int(arc4random()) % emoji.count
let e = emoji[choice]
let dateFormatter = DateFormatter()
dateFormatter.dateStyle = .medium
dateFormatter.timeStyle = .medium

let description = dateFormatter.string(from: d)
let len = description.count
let bar = String.init(repeating: "━", count: len + 2)

print("┏\(bar)┓")
print("┃ \(description) ┃ \(e)")
print("┗\(bar)┛")
