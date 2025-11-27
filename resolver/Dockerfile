FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY go.mod ./
# Ensure go.sum exists and deps are downloaded
RUN apk add --no-cache git
RUN go mod tidy
RUN go mod download

COPY . .
ENV CGO_ENABLED=0
RUN go build -v -o resolver main.go

FROM alpine:latest

WORKDIR /app
COPY --from=builder /app/resolver .

EXPOSE 5353/udp
EXPOSE 5353/tcp

CMD ["./resolver"]
