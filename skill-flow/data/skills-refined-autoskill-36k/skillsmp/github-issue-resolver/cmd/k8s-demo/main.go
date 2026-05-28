package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/openshift-aiops/openshift-cluster-health-mcp/pkg/clients"
)

func main() {
	fmt.Println("Kubernetes Client Demo")
	fmt.Println("=====================")
	fmt.Println()

	// Create Kubernetes client
	client, err := clients.NewK8sClient(nil)
	if err != nil {
		log.Fatalf("Failed to create Kubernetes client: %v", err)
	}
	defer func() {
		if err := client.Close(); err != nil {
			log.Printf("Error closing client: %v", err)
		}
	}()

	ctx := context.Background()

	// 1. Get server version
	fmt.Println("1. Server Version")
	fmt.Println("   ---------------")
	version, err := client.GetServerVersion(ctx)
	if err != nil {
		log.Printf("   Error: %v", err)
	} else {
		fmt.Printf("   %s\n", version)
	}
	fmt.Println()

	// 2. List nodes
	fmt.Println("2. Nodes")
	fmt.Println("   -----")
	nodes, err := client.ListNodes(ctx)
	if err != nil {
		log.Printf("   Error: %v", err)
	} else {
		fmt.Printf("   Total: %d nodes\n", len(nodes.Items))
		for i, node := range nodes.Items {
			ready := "NotReady"
			for _, condition := range node.Status.Conditions {
				if condition.Type == "Ready" && condition.Status == "True" {
					ready = "Ready"
					break
				}
			}
			fmt.Printf("   [%d] %s - %s (%s)\n", i+1, node.Name, ready, node.Status.NodeInfo.KubeletVersion)
		}
	}
	fmt.Println()

	// 3. Get cluster health
	fmt.Println("3. Cluster Health")
	fmt.Println("   --------------")
	health, err := client.GetClusterHealth(ctx)
	if err != nil {
		log.Printf("   Error: %v", err)
	} else {
		// Pretty print JSON
		healthJSON, _ := json.MarshalIndent(health, "   ", "  ")
		fmt.Println(string(healthJSON))
	}
	fmt.Println()

	// 4. List namespaces (top 10)
	fmt.Println("4. Namespaces (top 10)")
	fmt.Println("   -------------------")
	namespaces, err := client.ListNamespaces(ctx)
	if err != nil {
		log.Printf("   Error: %v", err)
	} else {
		count := 10
		if len(namespaces.Items) < count {
			count = len(namespaces.Items)
		}
		for i := 0; i < count; i++ {
			ns := namespaces.Items[i]
			fmt.Printf("   [%d] %s (Phase: %s)\n", i+1, ns.Name, ns.Status.Phase)
		}
		if len(namespaces.Items) > 10 {
			fmt.Printf("   ... and %d more\n", len(namespaces.Items)-10)
		}
	}
	fmt.Println()

	// 5. Demo retry logic
	fmt.Println("5. Retry Logic Demo")
	fmt.Println("   ----------------")
	_, err = clients.WithRetry(ctx, client, func(c *clients.K8sClient) (interface{}, error) {
		return c.ListNodes(ctx)
	})
	if err != nil {
		log.Printf("   Error: %v", err)
	} else {
		fmt.Printf("   ✅ Successfully retrieved nodes with retry logic\n")
	}
	fmt.Println()

	fmt.Println("Demo complete!")
	os.Exit(0)
}
