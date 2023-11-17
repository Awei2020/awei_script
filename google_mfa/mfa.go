package main

import (
	"crypto/hmac"
	"crypto/sha1"
	"encoding/base32"
	"encoding/binary"
	"fmt"
	"os/exec"
	"strings"
	"time"
)

func generateCode(token string) string {
	key, err := base32.StdEncoding.DecodeString(token)
	if err != nil {
		panic(err)
	}

	timestamp := uint64(time.Now().Unix()) / 30
	pack := make([]byte, 8)
	binary.BigEndian.PutUint64(pack, timestamp)

	sha := hmac.New(sha1.New, key)
	sha.Write(pack)
	hash := sha.Sum(nil)

	offset := int(hash[19] & 15)
	pwd := (binary.BigEndian.Uint32(hash[offset:offset+4]) & 0x7fffffff) % 1000000

	code := fmt.Sprintf("%06d", pwd)
	return code
}

func copyToClipboard(text string) {
	cmd := exec.Command("clip") // Windows command to copy to clipboard
	cmd.Stdin = strings.NewReader(text)
	err := cmd.Run()
	if err != nil {
		fmt.Println("Error copying to clipboard:", err)
	}
}

func main() {
	token := "xxxxxxxxxxxxxxxxxxx"
	code := generateCode(token)
	fmt.Println("Generated code:", code)
	copyToClipboard(code)
	fmt.Println("Code copied to clipboard!")
}
