// prints a block with the current time
package main

import (
	"fmt"
	"math/rand"
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

	time := fmt.Sprint(time.Now())[:19]
	emoji := emojis[rng.Intn(len(emojis))]

	fmt.Println("┏━━━━━━━━━━━━━━━━━━━━━━━━━┓")
	fmt.Printf("┃   %s   ┃ %s\n", time, emoji)
	fmt.Println("┗━━━━━━━━━━━━━━━━━━━━━━━━━┛")
}
