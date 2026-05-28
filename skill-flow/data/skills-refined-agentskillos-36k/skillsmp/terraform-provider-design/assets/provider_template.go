// Copyright (c) HashiCorp, Inc.
// SPDX-License-Identifier: MPL-2.0

package provider

import (
	"context"
	"os"

	"github.com/hashicorp/terraform-plugin-framework/datasource"
	"github.com/hashicorp/terraform-plugin-framework/provider"
	"github.com/hashicorp/terraform-plugin-framework/provider/schema"
	"github.com/hashicorp/terraform-plugin-framework/resource"
	"github.com/hashicorp/terraform-plugin-framework/types"
)

// Ensure ExampleProvider satisfies various provider interfaces.
var _ provider.Provider = &ExampleProvider{}

// ExampleProvider defines the provider implementation.
type ExampleProvider struct {
	// version is set to the provider version on release, "dev" when the
	// provider is built and ran locally, and "test" when running acceptance testing.
	version string
}

// ExampleProviderModel describes the provider data model.
type ExampleProviderModel struct {
	Endpoint types.String `tfsdk:"endpoint"`
	APIKey   types.String `tfsdk:"api_key"`
}

func (p *ExampleProvider) Metadata(ctx context.Context, req provider.MetadataRequest, resp *provider.MetadataResponse) {
	resp.TypeName = "example"
	resp.Version = p.version
}

func (p *ExampleProvider) Schema(ctx context.Context, req provider.SchemaRequest, resp *provider.SchemaResponse) {
	resp.Schema = schema.Schema{
		MarkdownDescription: "Example provider for managing resources via the Example API",
		Attributes: map[string]schema.Attribute{
			"endpoint": schema.StringAttribute{
				MarkdownDescription: "API endpoint URL. Can also be set via EXAMPLE_ENDPOINT environment variable.",
				Optional:            true,
			},
			"api_key": schema.StringAttribute{
				MarkdownDescription: "API key for authentication. Can also be set via EXAMPLE_API_KEY environment variable.",
				Optional:            true,
				Sensitive:           true,
			},
		},
	}
}

func (p *ExampleProvider) Configure(ctx context.Context, req provider.ConfigureRequest, resp *provider.ConfigureResponse) {
	var data ExampleProviderModel

	resp.Diagnostics.Append(req.Config.Get(ctx, &data)...)

	if resp.Diagnostics.HasError() {
		return
	}

	// Configuration values are now available.
	// If configuration values are not provided, use environment variables.

	endpoint := os.Getenv("EXAMPLE_ENDPOINT")
	apiKey := os.Getenv("EXAMPLE_API_KEY")

	if !data.Endpoint.IsNull() {
		endpoint = data.Endpoint.ValueString()
	}

	if !data.APIKey.IsNull() {
		apiKey = data.APIKey.ValueString()
	}

	// Validate required configuration
	if endpoint == "" {
		resp.Diagnostics.AddAttributeError(
			req.Config.AttributePath(ctx, "endpoint"),
			"Missing API Endpoint Configuration",
			"The provider requires an API endpoint to be configured. "+
				"Set the endpoint value in the configuration or use the EXAMPLE_ENDPOINT environment variable.",
		)
	}

	if apiKey == "" {
		resp.Diagnostics.AddAttributeError(
			req.Config.AttributePath(ctx, "api_key"),
			"Missing API Key Configuration",
			"The provider requires an API key to be configured. "+
				"Set the api_key value in the configuration or use the EXAMPLE_API_KEY environment variable.",
		)
	}

	if resp.Diagnostics.HasError() {
		return
	}

	// Create API client
	// client := NewAPIClient(endpoint, apiKey)

	// Make the client available during DataSource and Resource type Configure methods.
	// resp.DataSourceData = client
	// resp.ResourceData = client
}

func (p *ExampleProvider) Resources(ctx context.Context) []func() resource.Resource {
	return []func() resource.Resource{
		NewExampleResource,
		// Add more resources here
	}
}

func (p *ExampleProvider) DataSources(ctx context.Context) []func() datasource.DataSource {
	return []func() datasource.DataSource{
		NewExampleDataSource,
		// Add more data sources here
	}
}

func New(version string) func() provider.Provider {
	return func() provider.Provider {
		return &ExampleProvider{
			version: version,
		}
	}
}
