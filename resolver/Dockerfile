FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod ./
# COPY go.sum ./
# RUN go mod download

COPY . .
RUN go build -o resolver main.go

FROM alpine:latest

WORKDIR /app
COPY --from=builder /app/resolver .

EXPOSE 5353/udp
EXPOSE 5353/tcp

CMD ["./resolver"]
