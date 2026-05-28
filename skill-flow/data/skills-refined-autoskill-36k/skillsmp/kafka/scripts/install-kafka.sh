#!/bin/bash

# Script to install Apache Kafka on your system
# This script downloads, configures, and sets up a local Kafka environment

INSTALL_PATH="/opt/kafka"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--path)
            INSTALL_PATH="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [-p|--path INSTALL_PATH]"
            echo "  -p, --path: Installation path (default: /opt/kafka)"
            echo "  -h, --help: Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [-p|--path INSTALL_PATH]"
            exit 1
            ;;
    esac
done

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Apache Kafka installation..."
echo "Installing to: $INSTALL_PATH"

# Check if Java is installed (Java 17+ required)
java_available=false
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    MAJOR_VERSION=$(echo $JAVA_VERSION | cut -d'.' -f1)

    if [ "$MAJOR_VERSION" -ge 17 ]; then
        echo "Java version $JAVA_VERSION detected. Proceeding with native installation..."
        java_available=true
    else
        echo "Java version $JAVA_VERSION detected, but Java 17 or higher is required."
    fi
else
    echo "Java is not installed."
fi

# Check if Docker is available
docker_available=false
if command -v docker &> /dev/null; then
    echo "Docker is available."
    docker_available=true
else
    echo "Docker is not available."
fi

# If neither Java nor Docker is available, exit with error
if [ "$java_available" = false ] && [ "$docker_available" = false ]; then
    echo "ERROR: Neither Java 17+ nor Docker is available." >&2
    echo "Please install either:" >&2
    echo "  1. Java 17 or higher, or" >&2
    echo "  2. Docker" >&2
    exit 1
fi

# If Java is available, proceed with native installation
if [ "$java_available" = true ]; then
    echo "Proceeding with native Kafka installation..."
elif [ "$docker_available" = true ]; then
    echo "Java not available, but Docker is available. Starting Kafka with Docker..."

    # Check if Kafka container is already running
    if [ "$(docker ps -q -f name=kafka)" ]; then
        echo "Kafka container is already running."
        echo "Stopping existing Kafka container..."
        docker stop kafka 2>/dev/null
    fi

    # Check if Docker daemon is running
    if ! docker ps >/dev/null 2>&1; then
        echo "Docker daemon is not running. Please start Docker Desktop/Docker Engine first." >&2
        echo "On Windows with WSL2, make sure Docker Desktop is running and WSL integration is enabled." >&2
        echo "On Linux/macOS, ensure Docker service is running." >&2
        echo "Once Docker is started, please run this script again." >&2
        exit 1
    fi

    # Start Kafka using Docker
    echo "Starting Kafka using Docker..."
    docker run -d --name kafka -p 9092:9092 \
        -e KAFKA_NODE_ID=1 \
        -e KAFKA_PROCESS_ROLES=broker,controller \
        -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@127.0.0.1:9093 \
        -e KAFKA_LISTENERS=CLIENT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093 \
        -e KAFKA_ADVERTISED_LISTENERS=CLIENT://localhost:9092 \
        -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,CONTROLLER:PLAINTEXT \
        -e KAFKA_INTER_BROKER_LISTENER_NAME=CLIENT \
        -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
        -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
        -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 \
        -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
        -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
        -e KAFKA_JMX_PORT=9101 \
        apache/kafka:4.1.1

    exit_code=$?

    # Wait a moment for container to start
    sleep 5

    # Check if container is running
    if [ "$(docker ps -q -f name=kafka -f status=running)" ]; then
        echo "Kafka is now running in Docker container!"
        echo "Broker is available at localhost:9092"

        # Provide basic usage instructions
        echo ""
        echo "Basic Kafka commands for Docker:"
        echo "  Create topic: docker exec kafka kafka-topics --create --topic quickstart-events --bootstrap-server localhost:9092"
        echo "  Send messages: docker exec -i kafka kafka-console-producer --topic quickstart-events --bootstrap-server localhost:9092"
        echo "  Receive messages: docker exec -i kafka kafka-console-consumer --topic quickstart-events --from-beginning --bootstrap-server localhost:9092"
        echo "  Stop Kafka: docker stop kafka"
        echo "  Start Kafka again: docker start kafka"
        echo "  Remove container: docker rm kafka"

        exit 0
    else
        echo "Failed to start Kafka container. Docker Desktop/Docker Engine may not be running." >&2
        echo "Please ensure Docker is running before executing this script." >&2
        exit $exit_code
    fi
else
    # Neither Java nor Docker available
    echo "ERROR: Neither Java 17+ nor Docker is available." >&2
    echo "Please install either Java 17+ or Docker to proceed." >&2
    exit 1
fi

# If we reach this point, Java is available and we're proceeding with native installation

# Check if running as root for system installation
if [[ "$INSTALL_PATH" == /opt/* ]] || [[ "$INSTALL_PATH" == /usr/* ]]; then
    if [[ $EUID -ne 0 ]]; then
        echo "WARNING: This script is not running as root. Installation to $INSTALL_PATH may fail."
        echo "Consider running with sudo for system directory installation."
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Installation cancelled by user."
            exit 1
        fi
    fi
fi

# Create installation directory if it doesn't exist
INSTALL_DIR=$(dirname "$INSTALL_PATH")
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Creating directory: $INSTALL_DIR"
    sudo mkdir -p "$INSTALL_DIR"
fi

# Change to installation directory
cd "$INSTALL_DIR"

# Kafka version to install
KAFKA_VERSION="4.1.1"
SCALA_VERSION="2.13"
FILENAME="kafka_$SCALA_VERSION-$KAFKA_VERSION.tgz"
DOWNLOAD_URL="https://downloads.apache.org/kafka/$KAFKA_VERSION/$FILENAME"

echo "Downloading Kafka $KAFKA_VERSION..."

# Download Kafka
if command -v wget &> /dev/null; then
    wget $DOWNLOAD_URL
elif command -v curl &> /dev/null; then
    curl -O $DOWNLOAD_URL
else
    echo "ERROR: Neither wget nor curl is available. Please install one of them."
    exit 1
fi

# Extract Kafka
echo "Extracting Kafka..."
tar -xzf $FILENAME
KAFKA_DIR="kafka_$SCALA_VERSION-$KAFKA_VERSION"

# Move extracted directory to the specified install path
if [ -d "$INSTALL_PATH" ]; then
    echo "Removing existing Kafka installation at: $INSTALL_PATH"
    rm -rf "$INSTALL_PATH"
fi

mv "$KAFKA_DIR" "$INSTALL_PATH"

echo "Setting up Kafka environment..."

# Change to Kafka directory
cd "$INSTALL_PATH"

# Generate a Cluster UUID
echo "Generating cluster ID..."
export KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
echo "Generated cluster ID: $KAFKA_CLUSTER_ID"

# Format Log Directories
echo "Formatting log directories..."
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties

echo ""
echo "Kafka installation completed successfully!"
echo ""
echo "Installed to: $INSTALL_PATH"
echo ""
echo "To start the Kafka server, run:"
echo "  cd '$INSTALL_PATH'"
echo "  bin/kafka-server-start.sh config/server.properties"
echo ""
echo "To test your installation:"
echo "1. In a new terminal, start the Kafka server (command above)"
echo "2. Create a topic: bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092"
echo "3. Send messages: bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092"
echo "4. Receive messages: bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092"
echo ""
echo "To stop the Kafka server, press Ctrl+C in the server terminal."
echo ""

# Create a simple startup script
cat > "$INSTALL_PATH/start-kafka.sh" << EOF
#!/bin/bash
# Simple script to start Kafka server
export KAFKA_HOME='$INSTALL_PATH'

if [ ! -f "\$KAFKA_HOME/config/server.properties" ]; then
    echo "ERROR: config/server.properties not found in \$KAFKA_HOME."
    echo "Make sure this script is in the Kafka installation directory or KAFKA_HOME is set correctly."
    exit 1
fi

echo "Starting Kafka server in \$KAFKA_HOME..."
cd "\$KAFKA_HOME"
export KAFKA_CLUSTER_ID="\$(bin/kafka-storage.sh random-uuid 2>/dev/null)"
echo "Generated cluster ID: \$KAFKA_CLUSTER_ID"
bin/kafka-storage.sh format --standalone -t \$KAFKA_CLUSTER_ID -c config/server.properties 2>/dev/null
bin/kafka-server-start.sh config/server.properties
EOF

chmod +x "$INSTALL_PATH/start-kafka.sh"
echo "Created start-kafka.sh script for easy server startup."

# Create a simple test script
cat > "$INSTALL_PATH/test-kafka.sh" << EOF
#!/bin/bash
# Simple script to test Kafka installation
export KAFKA_HOME='$INSTALL_PATH'

echo "Testing Kafka installation in \$KAFKA_HOME..."

echo "Creating test topic..."
\$KAFKA_HOME/bin/kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 2>/dev/null

echo "Sending test message..."
echo "Hello Kafka!" | \$KAFKA_HOME/bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092 2>/dev/null &

sleep 2

echo "Receiving test message..."
timeout 10s \$KAFKA_HOME/bin/kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092 2>/dev/null

echo "Test completed!"
EOF

chmod +x "$INSTALL_PATH/test-kafka.sh"
echo "Created test-kafka.sh script to verify your installation works."

echo ""
echo "Installation Summary:"
echo "- Kafka installed to: $INSTALL_PATH"
echo "- Startup script: $INSTALL_PATH/start-kafka.sh"
echo "- Test script: $INSTALL_PATH/test-kafka.sh"
echo ""