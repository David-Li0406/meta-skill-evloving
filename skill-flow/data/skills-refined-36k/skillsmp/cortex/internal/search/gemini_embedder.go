package search

import (
	"context"
	"errors"

	"github.com/Napageneral/cortex/internal/gemini"
)

// GeminiEmbedder wraps the Gemini client for embedding queries.
type GeminiEmbedder struct {
	Client *gemini.Client
}

// Embed generates an embedding for the given query text.
func (g *GeminiEmbedder) Embed(query string, model string) ([]float64, error) {
	if g == nil || g.Client == nil {
		return nil, errors.New("gemini embedder not configured")
	}
	if model == "" {
		model = "gemini-embedding-001"
	}
	ctx := context.Background()
	resp, err := g.Client.EmbedContent(ctx, &gemini.EmbedContentRequest{
		Model: model,
		Content: gemini.Content{
			Parts: []gemini.Part{{Text: query}},
		},
	})
	if err != nil {
		return nil, err
	}
	if resp.Embedding == nil || len(resp.Embedding.Values) == 0 {
		return nil, errors.New("empty embedding response")
	}
	return resp.Embedding.Values, nil
}
