FROM golang:1.22.2

RUN mkdir -p /app/zenn

WORKDIR /app/zenn

COPY . .

RUN go install github.com/cespare/reflex@latest
RUN go install github.com/go-delve/delve/cmd/dlv@latest

CMD reflex -r '(\.go$|go\.mod)' -s go run *.go