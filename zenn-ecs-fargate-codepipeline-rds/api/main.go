package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func handler(c echo.Context) error {
	return c.JSON(http.StatusOK, map[string]string{"message": "hello"})
}

func newRouter() *echo.Echo {
	e := echo.New()
	e.GET("/", handler)
	return e
}

func main() {
	router := newRouter()
	router.Logger.Fatal(router.Start(":8888"))
}
