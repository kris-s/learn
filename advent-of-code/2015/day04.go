package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"log"
	"strings"
)

func main() {
	var startingInput string
	if _, err := fmt.Scanf("%s", &startingInput); err != nil {
		log.Fatal(err)
	}

	var count int
	for {
		input := fmt.Sprintf("%s%d", startingInput, count)
		hashFunc := md5.New()
		io.WriteString(hashFunc, input)
		hash := fmt.Sprintf("%x", hashFunc.Sum(nil))

		if strings.HasPrefix(hash, "000000") {
			fmt.Println(input)
			break
		}
		count++
	}
}
