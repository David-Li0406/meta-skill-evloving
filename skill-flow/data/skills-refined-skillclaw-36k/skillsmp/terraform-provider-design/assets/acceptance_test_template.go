// Copyright (c) HashiCorp, Inc.
// SPDX-License-Identifier: MPL-2.0

package provider

import (
	"fmt"
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestAccExampleResource(t *testing.T) {
	resource.Test(t, resource.TestCase{
		PreCheck:                 func() { testAccPreCheck(t) },
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			// Create and Read testing
			{
				Config: testAccExampleResourceConfig("test-example"),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("example_resource.test", "name", "test-example"),
					resource.TestCheckResourceAttrSet("example_resource.test", "id"),
					resource.TestCheckResourceAttrSet("example_resource.test", "last_updated"),
				),
			},
			// ImportState testing
			{
				ResourceName:      "example_resource.test",
				ImportState:       true,
				ImportStateVerify: true,
				// Ignore computed-only fields that can't be imported
				ImportStateVerifyIgnore: []string{"last_updated"},
			},
			// Update and Read testing
			{
				Config: testAccExampleResourceConfig("test-example-updated"),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("example_resource.test", "name", "test-example-updated"),
				),
			},
			// Delete testing automatically occurs in TestCase
		},
	})
}

func testAccExampleResourceConfig(name string) string {
	return fmt.Sprintf(`
resource "example_resource" "test" {
  name        = %[1]q
  description = "Test resource for acceptance testing"
}
`, name)
}

// TestAccExampleDataSource tests the data source
func TestAccExampleDataSource(t *testing.T) {
	resource.Test(t, resource.TestCase{
		PreCheck:                 func() { testAccPreCheck(t) },
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			// Read testing
			{
				Config: testAccExampleDataSourceConfig,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("data.example_data.test", "name", "test-lookup"),
					resource.TestCheckResourceAttrSet("data.example_data.test", "id"),
					resource.TestCheckResourceAttrSet("data.example_data.test", "description"),
				),
			},
		},
	})
}

const testAccExampleDataSourceConfig = `
data "example_data" "test" {
  name = "test-lookup"
}
`
