// draws a unique block to your terminal to help separate long output
// daily-go for 2015-11-3
package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))

	symbols := map[int]string{
		1:  "🙂",
		2:  "🐶",
		3:  "🦁",
		4:  "🐺",
		5:  "🐉",
		6:  "🐘",
		7:  "🌺",
		8:  "🍁",
		9:  "🍦",
		10: "🍓",
		11: "🍏",
		12: "🚗",
		13: "⛵",
	}

	top := "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
	mid := "┃      "
	btm := "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
	mid += fmt.Sprint(time.Now())[:19]
	mid += "      ┃ "
	mid += symbols[r.Intn(12)+1]

	fmt.Println(top)
	fmt.Println(mid)
	fmt.Println(btm)
}
