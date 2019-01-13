package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"time"
)

type Config struct {
	Name  string
	Token string
	Host  string
	Port  int
}

func main() {
	nameP := flag.String("n", "client", "name")
	tokenP := flag.String("t", "notoken", "token")
	hostP := flag.String("h", "localhost", "host")
	portP := flag.Int("p", 2333, "port")
	flag.Parse()

	var conf Config
	if *tokenP != "notoken" {
		// save config
		conf.Name = *nameP
		conf.Token = *tokenP
		conf.Host = *hostP
		conf.Port = *portP
		file, err := os.Create("httpcallbackconfig.json")
		if err != nil {
			panic(err)
		}
		defer file.Close()
		encoder := json.NewEncoder(file)
		err = encoder.Encode(conf)
		if err != nil {
			panic(err)
		}

	} else {
		// load config
		file, err := os.Open("httpcallbackconfig.json")
		if err != nil {
			panic(err)
		}
		defer file.Close()
		decoder := json.NewDecoder(file)
		err = decoder.Decode(&conf)
		if err != nil {
			panic(err)
		}
		nameP = &conf.Name
		tokenP = &conf.Token
		hostP = &conf.Host
		portP = &conf.Port
	}

	fmt.Fprintln(os.Stderr, *nameP)
	fmt.Fprintln(os.Stderr, "token", *tokenP)
	fmt.Fprintln(os.Stderr, *hostP, *portP)

	resp, err := http.Get(fmt.Sprintf("http://%s:%d/%s?token=%s&msg=start",
		*hostP, *portP, *nameP, *tokenP))
	if err != nil {
		panic(err)
		os.Exit(1)
	}
	if resp.StatusCode != 200 {
		println(resp.StatusCode)
		os.Exit(1)
	}

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		if err := scanner.Err(); err != nil {
			panic(err)
			os.Exit(1)
		}
		s := scanner.Text()
		fmt.Println(s)
		s = fmt.Sprintf("[%v]\n%s", time.Now(), s)
		s = url.QueryEscape(s)
		resp, err := http.Get(fmt.Sprintf("http://%s:%d/%s?token=%s&msg=%s",
			*hostP, *portP, *nameP, *tokenP, s))
		if err != nil || resp.StatusCode != 200 {
			println("failed")
		}
	}
}
