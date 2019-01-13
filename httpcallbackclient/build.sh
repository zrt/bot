#!/bin/bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o httpcallback-linux  main.go
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o httpcallback-win.exe  main.go
CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -o httpcallback-mac  main.go 
