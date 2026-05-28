package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

// HelloResponse is the response for the hello endpoint
type HelloResponse struct {
	Message string `json:"message"`
}

func main() {
	r := chi.NewRouter()

	// middleware
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	// routes
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("welcome to go-starter"))
	})

	r.Get("/api/hello", func(w http.ResponseWriter, r *http.Request) {
		response := HelloResponse{
			Message: "Hello from Go!",
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	r.Get("/api/hello/{name}", func(w http.ResponseWriter, r *http.Request) {
		name := chi.URLParam(r, "name")
		response := HelloResponse{
			Message: "Hello, " + name + "!",
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	// health check
	r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("ok"))
	})

	log.Println("starting server on :8080")
	log.Fatal(http.ListenAndServe(":8080", r))
}
