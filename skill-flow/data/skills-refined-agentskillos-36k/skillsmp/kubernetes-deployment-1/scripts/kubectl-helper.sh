#!/bin/bash
# kubectl-helper.sh - Helper script for common Kubernetes operations

set -e

function help_message() {
    echo "Kubernetes Helper Script"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  setup-minikube    - Set up a local Minikube cluster with recommended settings"
    echo "  deploy-app        - Deploy an application using kubectl"
    echo "  deploy-helm       - Deploy an application using Helm"
    echo "  check-status      - Check the status of deployments and services"
    echo "  scale-app         - Scale a deployment"
    echo "  port-forward      - Port forward to a service for local testing"
    echo "  logs              - Get logs from a deployment"
    echo "  delete-app        - Delete an application"
    echo "  help              - Show this help message"
}

function setup_minikube() {
    echo "Setting up Minikube with recommended settings..."
    minikube start --cpus=4 --memory=8192 --disk-size=20g

    echo "Enabling required addons..."
    minikube addons enable ingress
    minikube addons enable metrics-server

    echo "Minikube setup complete!"
    echo "Current context: $(kubectl config current-context)"
}

function check_status() {
    echo "Checking cluster status..."
    kubectl cluster-info
    echo ""

    echo "Checking nodes..."
    kubectl get nodes
    echo ""

    echo "Checking deployments..."
    kubectl get deployments
    echo ""

    echo "Checking services..."
    kubectl get services
    echo ""

    echo "Checking pods..."
    kubectl get pods
}

case "${1:-help}" in
    "setup-minikube")
        setup_minikube
        ;;
    "check-status")
        check_status
        ;;
    "help")
        help_message
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        help_message
        exit 1
        ;;
esac
