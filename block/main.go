// prints a block with the current time
package main

import (
	"fmt"
	"math/rand"
	"strings"
	"time"
)

func main() {
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))

	emojis := []string{
		"🙂",
		"👹",
		"☠️",
		"🧶",
		"🐶",
		"🦄",
		"🐝",
		"🦋",
		"🦑",
		"🦖",
		"🐳",
		"🌳",
		"🌿",
		"🌺",
		"🌙",
		"⭐️",
		"🔥",
		"🌈",
		"⚡️",
		"🌊",
		"🍉",
		"🌶",
		"🧩",
		"⚔️",
		"🛡",
		"🧿",
		"🧬",
		"💝",
		"🔸",
		"🏴‍☠️",
	}

	now := time.Now()
	time := now.Format("Monday, 2 January 2006    15:04:05")
	emoji := emojis[rng.Intn(len(emojis))]
	bar := strings.Repeat("━", len(time)+6)

	fmt.Printf("┏%s┓\n", bar)
	fmt.Printf("┃   %s   ┃ %s\n", time, emoji)
	fmt.Printf("┗%s┛\n", bar)

}
