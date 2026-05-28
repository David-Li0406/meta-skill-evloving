#!/bin/bash
# Kafka utility script for common operations

# Function to create a topic
create_topic() {
    local topic_name=$1
    local partitions=${2:-3}
    local replication_factor=${3:-1}

    echo "Creating topic: $topic_name with $partitions partitions and replication factor $replication_factor"
    kafka-topics --create \
        --topic "$topic_name" \
        --bootstrap-server localhost:9092 \
        --partitions "$partitions" \
        --replication-factor "$replication_factor"
}

# Function to list all topics
list_topics() {
    echo "Listing all topics:"
    kafka-topics --list --bootstrap-server localhost:9092
}

# Function to describe a topic
describe_topic() {
    local topic_name=$1
    echo "Describing topic: $topic_name"
    kafka-topics --describe --topic "$topic_name" --bootstrap-server localhost:9092
}

# Function to consume messages from a topic
consume_messages() {
    local topic_name=$1
    local group_id=${2:-console-consumer-$(date +%s)}

    echo "Consuming messages from topic: $topic_name (consumer group: $group_id)"
    kafka-console-consumer --bootstrap-server localhost:9092 \
        --topic "$topic_name" \
        --from-beginning \
        --group "$group_id"
}

# Function to produce messages to a topic
produce_messages() {
    local topic_name=$1

    echo "Producing messages to topic: $topic_name (Press Ctrl+C to stop)"
    kafka-console-producer --bootstrap-server localhost:9092 --topic "$topic_name"
}

# Function to check consumer group status
check_consumer_group() {
    local group_id=$1

    echo "Checking consumer group: $group_id"
    kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group "$group_id"
}

# Display help
show_help() {
    echo "Kafka Utility Script"
    echo ""
    echo "Usage: $0 [command] [arguments]"
    echo ""
    echo "Commands:"
    echo "  create-topic <topic-name> [partitions] [replication-factor] - Create a new topic"
    echo "  list-topics                                               - List all topics"
    echo "  describe-topic <topic-name>                               - Describe a topic"
    echo "  consume <topic-name> [group-id]                           - Consume messages from topic"
    echo "  produce <topic-name>                                      - Produce messages to topic"
    echo "  check-group <group-id>                                    - Check consumer group status"
    echo "  help                                                      - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 create-topic my-test-topic 6 1"
    echo "  $0 list-topics"
    echo "  $0 consume my-test-topic"
    echo "  $0 produce my-test-topic"
}

# Main script logic
case "$1" in
    "create-topic")
        if [ -z "$2" ]; then
            echo "Error: Topic name is required"
            show_help
            exit 1
        fi
        create_topic "$2" "$3" "$4"
        ;;
    "list-topics")
        list_topics
        ;;
    "describe-topic")
        if [ -z "$2" ]; then
            echo "Error: Topic name is required"
            show_help
            exit 1
        fi
        describe_topic "$2"
        ;;
    "consume")
        if [ -z "$2" ]; then
            echo "Error: Topic name is required"
            show_help
            exit 1
        fi
        consume_messages "$2" "$3"
        ;;
    "produce")
        if [ -z "$2" ]; then
            echo "Error: Topic name is required"
            show_help
            exit 1
        fi
        produce_messages "$2"
        ;;
    "check-group")
        if [ -z "$2" ]; then
            echo "Error: Group ID is required"
            show_help
            exit 1
        fi
        check_consumer_group "$2"
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