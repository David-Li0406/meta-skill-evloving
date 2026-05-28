# PowerShell script to install Apache Kafka on Windows
# This script downloads, configures, and sets up a local Kafka environment
param(
    [Parameter(Mandatory=$false)]
    [string]$InstallPath = "C:\Program Files\kafka"
)

Write-Host "Starting Apache Kafka installation..." -ForegroundColor Green
Write-Host "Installing to: $InstallPath" -ForegroundColor Cyan

# Check if running as Administrator (needed for Program Files installation)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: This script is not running as Administrator. Installation to Program Files may fail." -ForegroundColor Yellow
    Write-Host "Consider running PowerShell as Administrator for Program Files installation." -ForegroundColor Yellow
    $choice = Read-Host "Continue anyway? (y/n)"
    if ($choice -ne 'y' -and $choice -ne 'Y') {
        Write-Host "Installation cancelled by user." -ForegroundColor Red
        exit 1
    }
}

# Check if Java is installed (Java 17+ required)
$java_available = $false
try {
    $java_version_output = java -version 2>&1
    $java_version_line = $java_version_output | Where-Object { $_ -match "version" } | Select-Object -First 1
    if ($java_version_line -match '"([^"]+)"') {
        $java_version = $matches[1]
        Write-Host "Java version detected: $java_version" -ForegroundColor Green

        # Extract major version
        $major_version = [int]$java_version.split('.')[0]
        if ($major_version -ge 17) {
            Write-Host "Java 17 or higher is available. Proceeding with native installation..." -ForegroundColor Green
            $java_available = $true
        } else {
            Write-Host "Java version $java_version detected, but Java 17 or higher is required." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Could not determine Java version." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Java is not installed." -ForegroundColor Yellow
}

# Check if Docker is available
$docker_available = $false
try {
    $docker_version = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Docker is available." -ForegroundColor Green
        $docker_available = $true
    }
} catch {
    Write-Host "Docker is not available." -ForegroundColor Yellow
}

# If neither Java nor Docker is available, exit with error
if (-not $java_available -and -not $docker_available) {
    Write-Host "ERROR: Neither Java 17+ nor Docker is available." -ForegroundColor Red
    Write-Host "Please install either:" -ForegroundColor Red
    Write-Host "  1. Java 17 or higher, or" -ForegroundColor Red
    Write-Host "  2. Docker Desktop" -ForegroundColor Red
    exit 1
}

# If Java is available, proceed with native installation
if ($java_available) {
    Write-Host "Proceeding with native Kafka installation..." -ForegroundColor Green
} elseif ($docker_available) {
    Write-Host "Java not available, but Docker is available. Starting Kafka with Docker..." -ForegroundColor Yellow

    # Check if Kafka container is already running
    $container_exists = docker ps -q -f name=kafka 2>$null
    if ($container_exists) {
        Write-Host "Kafka container is already running." -ForegroundColor Yellow
        Write-Host "Stopping existing Kafka container..." -ForegroundColor Yellow
        docker stop kafka 2>$null
    }

    # Check if Docker daemon is running
    try {
        $docker_ps_result = docker ps 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Docker daemon is not running. Please start Docker Desktop first." -ForegroundColor Red
            Write-Host "On Windows, make sure Docker Desktop is running in the system tray." -ForegroundColor Yellow
            Write-Host "Once Docker Desktop is started, please run this script again." -ForegroundColor Yellow
            exit 1
        }
    } catch {
        Write-Host "Failed to communicate with Docker daemon. Please ensure Docker Desktop is running." -ForegroundColor Red
        exit 1
    }

    # Start Kafka using Docker
    Write-Host "Starting Kafka using Docker..." -ForegroundColor Green
    $docker_cmd = "docker run -d --name kafka -p 9092:9092 " +
                  "-e KAFKA_NODE_ID=1 " +
                  "-e KAFKA_PROCESS_ROLES=broker,controller " +
                  "-e KAFKA_CONTROLLER_QUORUM_VOTERS=1@127.0.0.1:9093 " +
                  "-e KAFKA_LISTENERS=CLIENT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093 " +
                  "-e KAFKA_ADVERTISED_LISTENERS=CLIENT://localhost:9092 " +
                  "-e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,CONTROLLER:PLAINTEXT " +
                  "-e KAFKA_INTER_BROKER_LISTENER_NAME=CLIENT " +
                  "-e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER " +
                  "-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 " +
                  "-e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 " +
                  "-e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 " +
                  "-e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 " +
                  "-e KAFKA_JMX_PORT=9101 " +
                  "apache/kafka:4.1.1"

    Invoke-Expression $docker_cmd
    $exit_code = $LASTEXITCODE

    # Wait a moment for container to start
    Start-Sleep -Seconds 5

    # Check if container is running
    $container_running = docker ps --filter "name=kafka" --filter "status=running" --format "{{.Names}}" 2>$null
    if ($container_running -eq "kafka") {
        Write-Host "Kafka is now running in Docker container!" -ForegroundColor Green
        Write-Host "Broker is available at localhost:9092" -ForegroundColor Green

        # Provide basic usage instructions
        Write-Host "`nBasic Kafka commands for Docker:" -ForegroundColor Cyan
        Write-Host "  Create topic: docker exec kafka kafka-topics --create --topic quickstart-events --bootstrap-server localhost:9092" -ForegroundColor White
        Write-Host "  Send messages: docker exec -i kafka kafka-console-producer --topic quickstart-events --bootstrap-server localhost:9092" -ForegroundColor White
        Write-Host "  Receive messages: docker exec -i kafka kafka-console-consumer --topic quickstart-events --from-beginning --bootstrap-server localhost:9092" -ForegroundColor White
        Write-Host "  Stop Kafka: docker stop kafka" -ForegroundColor White
        Write-Host "  Start Kafka again: docker start kafka" -ForegroundColor White
        Write-Host "  Remove container: docker rm kafka" -ForegroundColor White

        exit 0
    } else {
        Write-Host "Failed to start Kafka container. Docker Desktop may not be running." -ForegroundColor Red
        Write-Host "Please ensure Docker Desktop is running in the system tray before executing this script." -ForegroundColor Yellow
        exit $exit_code
    }
} else {
    # Neither Java nor Docker available
    Write-Host "ERROR: Neither Java 17+ nor Docker is available." -ForegroundColor Red
    Write-Host "Please install either Java 17+ or Docker Desktop to proceed." -ForegroundColor Red
    exit 1
}

# If we reach this point, Java is available and we're proceeding with native installation

# Create installation directory if it doesn't exist
$installDir = Split-Path $InstallPath -Parent
if (!(Test-Path $installDir)) {
    Write-Host "Creating directory: $installDir" -ForegroundColor Green
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

# Change to installation directory
Set-Location $installDir

# Kafka version to install
$kafka_version = "4.1.1"
$scala_version = "2.13"
$filename = "kafka_$scala_version-$kafka_version.tgz"
$download_url = "https://downloads.apache.org/kafka/$kafka_version/$filename"

Write-Host "Downloading Kafka $kafka_version..." -ForegroundColor Green

# Download Kafka
Invoke-WebRequest -Uri $download_url -OutFile $filename

# Extract Kafka (PowerShell 5.0+ has Expand-Archive, but for .tar.gz we need a different approach)
Write-Host "Extracting Kafka..." -ForegroundColor Green

# Use tar command which is available on Windows 10+
tar -xzf $filename

$kafka_dir = "kafka_$scala_version-$kafka_version"
$final_install_path = Join-Path $installDir $kafka_dir

# Rename the extracted directory to the specified install path
if (Test-Path $final_install_path) {
    Write-Host "Removing existing Kafka installation at: $final_install_path" -ForegroundColor Yellow
    Remove-Item -Recurse -Force $final_install_path
}

Rename-Item -Path $kafka_dir -NewName (Split-Path $InstallPath -Leaf)

Write-Host "Kafka extracted to directory: $InstallPath" -ForegroundColor Green

# Change to Kafka directory
Set-Location $InstallPath

# Generate a Cluster UUID
Write-Host "Generating cluster ID..." -ForegroundColor Green
$cluster_id = .\bin\kafka-storage.bat random-uuid
Write-Host "Generated cluster ID: $cluster_id" -ForegroundColor Green

# Format Log Directories
Write-Host "Formatting log directories..." -ForegroundColor Green
.\bin\kafka-storage.bat format --standalone -t $cluster_id -c config\server.properties

Write-Host "" -ForegroundColor Green
Write-Host "Kafka installation completed successfully!" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "Installed to: $InstallPath" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Green
Write-Host "To start the Kafka server, run:" -ForegroundColor Yellow
Write-Host "  cd '$InstallPath'" -ForegroundColor White
Write-Host "  .\bin\kafka-server-start.bat config\server.properties" -ForegroundColor White
Write-Host "" -ForegroundColor Green
Write-Host "To test your installation:" -ForegroundColor Yellow
Write-Host "1. In a new terminal, start the Kafka server (command above)" -ForegroundColor White
Write-Host "2. Create a topic: .\bin\kafka-topics.bat --create --topic quickstart-events --bootstrap-server localhost:9092" -ForegroundColor White
Write-Host "3. Send messages: .\bin\kafka-console-producer.bat --topic quickstart-events --bootstrap-server localhost:9092" -ForegroundColor White
Write-Host "4. Receive messages: .\bin\kafka-console-consumer.bat --topic quickstart-events --from-beginning --bootstrap-server localhost:9092" -ForegroundColor White
Write-Host "" -ForegroundColor Green
Write-Host "To stop the Kafka server, press Ctrl+C in the server terminal." -ForegroundColor Yellow
Write-Host "" -ForegroundColor Green

# Create a simple startup script
$start_script_content = @"
@echo off
REM Simple script to start Kafka server
SET KAFKA_HOME=$InstallPath

if not exist "%KAFKA_HOME%\config\server.properties" (
    echo ERROR: config/server.properties not found in %%KAFKA_HOME%%.
    echo Make sure this script is in the Kafka installation directory or KAFKA_HOME is set correctly.
    pause
    exit /b 1
)

echo Starting Kafka server in %%KAFKA_HOME%%...
cd /d "%KAFKA_HOME%"
for /f "delims=" %%i in ('bin\kafka-storage.bat random-uuid') do set KAFKA_CLUSTER_ID=%%i
echo Generated cluster ID: %%KAFKA_CLUSTER_ID%%
bin\kafka-storage.bat format --standalone -t %%KAFKA_CLUSTER_ID%% -c config\server.properties > nul 2>&1
bin\kafka-server-start.bat config\server.properties
"@

Set-Content -Path "$InstallPath\start-kafka.bat" -Value $start_script_content
Write-Host "Created start-kafka.bat script for easy server startup." -ForegroundColor Green

# Create a simple test script
$test_script_content = @"
@echo off
REM Simple script to test Kafka installation
SET KAFKA_HOME=$InstallPath

echo Testing Kafka installation in %%KAFKA_HOME%%...
cd /d "%KAFKA_HOME%"

echo Creating test topic...
bin\kafka-topics.bat --create --topic test-topic --bootstrap-server localhost:9092 > nul 2>&1

echo Sending test message...
echo Hello Kafka! | bin\kafka-console-producer.bat --topic test-topic --bootstrap-server localhost:9092 > nul 2>&1

timeout /t 2 /nobreak > nul

echo Receiving test message...
echo Waiting for messages...
powershell -Command "try { bin\kafka-console-consumer.bat --topic test-topic --from-beginning --bootstrap-server localhost:9092 --timeout-ms 5000 } catch { Write-Host 'Timeout waiting for messages.' }"

echo Test completed!
"@

Set-Content -Path "$InstallPath\test-kafka.bat" -Value $test_script_content
Write-Host "Created test-kafka.bat script to verify your installation works." -ForegroundColor Green

Write-Host "" -ForegroundColor Green
Write-Host "Installation Summary:" -ForegroundColor Cyan
Write-Host "- Kafka installed to: $InstallPath" -ForegroundColor White
Write-Host "- Startup script: $InstallPath\start-kafka.bat" -ForegroundColor White
Write-Host "- Test script: $InstallPath\test-kafka.bat" -ForegroundColor White
Write-Host "" -ForegroundColor Green