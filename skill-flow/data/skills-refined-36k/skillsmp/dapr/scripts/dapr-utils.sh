#!/bin/bash
# DAPR utility script for common operations

# Function to run an application with DAPR sidecar
run_with_dapr() {
    local app_id=$1
    local app_port=$2
    local command=$3

    echo "Running application with DAPR sidecar: $app_id on port $app_port"
    dapr run --app-id "$app_id" --app-port "$app_port" $command
}

# Function to check DAPR status
check_dapr_status() {
    echo "Checking DAPR status..."
    dapr status
}

# Function to list running DAPR instances
list_dapr_instances() {
    echo "Listing running DAPR instances..."
    dapr list
}

# Function to stop a specific DAPR instance
stop_dapr_instance() {
    local app_id=$1

    echo "Stopping DAPR instance: $app_id"
    dapr stop --app-id "$app_id"
}

# Function to stop all DAPR instances
stop_all_dapr() {
    echo "Stopping all DAPR instances..."
    dapr stop --all
}

# Function to get DAPR configurations
get_dapr_configs() {
    echo "Getting DAPR configurations..."
    dapr configurations
}

# Function to get DAPR components
get_dapr_components() {
    echo "Getting DAPR components..."
    dapr components
}

# Function to publish a test message to a topic
publish_test_message() {
    local pubsub_name=$1
    local topic_name=$2
    local message=$3

    echo "Publishing test message to $pubsub_name/$topic_name: $message"
    curl -X POST http://localhost:3500/v1.0/publish/"$pubsub_name"/"$topic_name" \
         -H "Content-Type: application/json" \
         -d "$message"
}

# Function to save state
save_state() {
    local store_name=$1
    local key=$2
    local value=$3

    echo "Saving state to $store_name/$key: $value"
    curl -X POST http://localhost:3500/v1.0/state/"$store_name" \
         -H "Content-Type: application/json" \
         -d "[{\"key\":\"$key\",\"value\":$value}]"
}

# Function to get state
get_state() {
    local store_name=$1
    local key=$2

    echo "Getting state from $store_name/$key"
    curl http://localhost:3500/v1.0/state/"$store_name"/"$key"
}

# Function to check Kubernetes DAPR status
check_k8s_dapr_status() {
    echo "Checking DAPR status in Kubernetes..."
    dapr status -k
}

# Function to get Kubernetes DAPR components
get_k8s_dapr_components() {
    echo "Getting DAPR components in Kubernetes..."
    dapr components -k
}

# Function to get Kubernetes DAPR configurations
get_k8s_dapr_configs() {
    echo "Getting DAPR configurations in Kubernetes..."
    dapr configurations -k
}

# Display help
show_help() {
    echo "DAPR Utility Script"
    echo ""
    echo "Usage: $0 [command] [arguments]"
    echo ""
    echo "Commands:"
    echo "  run <app-id> <port> <command>     - Run application with DAPR sidecar"
    echo "  status                            - Check DAPR status"
    echo "  list                              - List running DAPR instances"
    echo "  stop <app-id>                     - Stop a specific DAPR instance"
    echo "  stop-all                          - Stop all DAPR instances"
    echo "  configs                           - Get DAPR configurations"
    echo "  components                        - Get DAPR components"
    echo "  publish <pubsub> <topic> <msg>    - Publish a test message"
    echo "  save-state <store> <key> <value>  - Save state to a store"
    echo "  get-state <store> <key>           - Get state from a store"
    echo "  k8s-status                        - Check DAPR status in Kubernetes"
    echo "  k8s-components                    - Get DAPR components in Kubernetes"
    echo "  k8s-configs                       - Get DAPR configurations in Kubernetes"
    echo "  help                              - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 run myapp 3000 \"node app.js\""
    echo "  $0 publish pubsub orders '{\"orderId\": 123}'"
    echo "  $0 save-state mystore user1 '{\"name\": \"John\"}'"
}

# Main script logic
case "$1" in
    "run")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "Error: Missing arguments for run command"
            show_help
            exit 1
        fi
        run_with_dapr "$2" "$3" "$4"
        ;;
    "status")
        check_dapr_status
        ;;
    "list")
        list_dapr_instances
        ;;
    "stop")
        if [ -z "$2" ]; then
            echo "Error: Missing app-id for stop command"
            show_help
            exit 1
        fi
        stop_dapr_instance "$2"
        ;;
    "stop-all")
        stop_all_dapr
        ;;
    "configs")
        get_dapr_configs
        ;;
    "components")
        get_dapr_components
        ;;
    "publish")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "Error: Missing arguments for publish command"
            show_help
            exit 1
        fi
        publish_test_message "$2" "$3" "$4"
        ;;
    "save-state")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "Error: Missing arguments for save-state command"
            show_help
            exit 1
        fi
        save_state "$2" "$3" "$4"
        ;;
    "get-state")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Error: Missing arguments for get-state command"
            show_help
            exit 1
        fi
        get_state "$2" "$3"
        ;;
    "k8s-status")
        check_k8s_dapr_status
        ;;
    "k8s-components")
        get_k8s_dapr_components
        ;;
    "k8s-configs")
        get_k8s_dapr_configs
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
