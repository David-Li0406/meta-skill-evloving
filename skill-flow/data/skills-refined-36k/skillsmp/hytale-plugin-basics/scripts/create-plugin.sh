#!/bin/bash

# Hytale Plugin Scaffolding Script
# Creates a basic Hytale server plugin project structure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}   Hytale Plugin Scaffolding Tool    ${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default values
DEFAULT_GROUP="com.example"
DEFAULT_VERSION="1.0.0"
DEFAULT_AUTHOR="Author"

print_header

# Get plugin name
if [ -z "$1" ]; then
    read -p "Plugin Name (e.g., MyAwesomePlugin): " PLUGIN_NAME
else
    PLUGIN_NAME="$1"
fi

if [ -z "$PLUGIN_NAME" ]; then
    print_error "Plugin name is required!"
    exit 1
fi

# Validate plugin name (1-64 chars, alphanumeric)
if ! [[ "$PLUGIN_NAME" =~ ^[a-zA-Z][a-zA-Z0-9]{0,63}$ ]]; then
    print_error "Plugin name must start with a letter, contain only alphanumeric characters, and be 1-64 characters long."
    exit 1
fi

# Get group/package
if [ -z "$2" ]; then
    read -p "Group/Package (default: $DEFAULT_GROUP): " GROUP
    GROUP=${GROUP:-$DEFAULT_GROUP}
else
    GROUP="$2"
fi

# Get version
if [ -z "$3" ]; then
    read -p "Version (default: $DEFAULT_VERSION): " VERSION
    VERSION=${VERSION:-$DEFAULT_VERSION}
else
    VERSION="$3"
fi

# Get author name
if [ -z "$4" ]; then
    read -p "Author Name (default: $DEFAULT_AUTHOR): " AUTHOR
    AUTHOR=${AUTHOR:-$DEFAULT_AUTHOR}
else
    AUTHOR="$4"
fi

# Get description
if [ -z "$5" ]; then
    read -p "Description (optional): " DESCRIPTION
else
    DESCRIPTION="$5"
fi

# Convert plugin name to lowercase for directory
PLUGIN_DIR_NAME=$(echo "$PLUGIN_NAME" | tr '[:upper:]' '[:lower:]')
PLUGIN_DIR="$PLUGIN_DIR_NAME"

# Convert group to directory path
PACKAGE_PATH=$(echo "$GROUP.$PLUGIN_DIR_NAME" | tr '.' '/')

print_info "Creating plugin: $PLUGIN_NAME"
print_info "Location: ./$PLUGIN_DIR"
echo ""

# Check if directory already exists
if [ -d "$PLUGIN_DIR" ]; then
    print_warning "Directory '$PLUGIN_DIR' already exists!"
    read -p "Overwrite? (y/N): " OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
        print_info "Aborted."
        exit 0
    fi
    rm -rf "$PLUGIN_DIR"
fi

# Create directory structure
print_info "Creating directory structure..."
mkdir -p "$PLUGIN_DIR/src/main/java/$PACKAGE_PATH/commands"
mkdir -p "$PLUGIN_DIR/src/main/java/$PACKAGE_PATH/events"
mkdir -p "$PLUGIN_DIR/src/main/java/$PACKAGE_PATH/components"
mkdir -p "$PLUGIN_DIR/src/main/java/$PACKAGE_PATH/systems"
mkdir -p "$PLUGIN_DIR/src/main/resources/assets/Server/Content"

# Create manifest.json
print_info "Creating manifest.json..."
cat > "$PLUGIN_DIR/src/main/resources/manifest.json" << EOF
{
  "Group": "$GROUP",
  "Name": "$PLUGIN_NAME",
  "Version": "$VERSION",
  "Description": "$DESCRIPTION",
  "Authors": [
    {
      "Name": "$AUTHOR"
    }
  ],
  "Main": "$GROUP.$PLUGIN_DIR_NAME.$PLUGIN_NAME",
  "ServerVersion": ">=1.0.0",
  "Dependencies": {},
  "OptionalDependencies": {},
  "DisabledByDefault": false,
  "IncludesAssetPack": false
}
EOF

# Create main plugin class
print_info "Creating main plugin class..."
cat > "$PLUGIN_DIR/src/main/java/$PACKAGE_PATH/$PLUGIN_NAME.java" << EOF
package $GROUP.$PLUGIN_DIR_NAME;

import com.hypixel.hytale.server.core.plugin.JavaPlugin;
import com.hypixel.hytale.server.core.plugin.JavaPluginInit;
import javax.annotation.Nonnull;

/**
 * Main plugin class for $PLUGIN_NAME.
 * 
 * Lifecycle:
 * - setup(): Called after config load. Register commands, events, components here.
 * - start(): Called after all plugins complete setup. Safe to interact with other plugins.
 * - shutdown(): Called before disable. Cleanup resources here.
 */
public class $PLUGIN_NAME extends JavaPlugin {
    
    public $PLUGIN_NAME(@Nonnull JavaPluginInit init) {
        super(init);
    }
    
    @Override
    protected void setup() {
        // Register commands, events, components, and systems here
        // Example: getCommandRegistry().registerCommand(new MyCommand());
        // Example: getEventRegistry().registerGlobal(PlayerConnectEvent.class, this::onPlayerConnect);
        
        getLogger().atInfo().log("$PLUGIN_NAME setup complete!");
    }
    
    @Override
    protected void start() {
        // Called after all plugins complete setup
        // Safe to interact with world, players, and other plugins here
        
        getLogger().atInfo().log("$PLUGIN_NAME started!");
    }
    
    @Override
    protected void shutdown() {
        // Cleanup resources, save data, cancel tasks here
        
        getLogger().atInfo().log("$PLUGIN_NAME shutting down!");
    }
}
EOF

# Create example command class
print_info "Creating example command..."
cat > "$PLUGIN_DIR/src/main/java/$PACKAGE_PATH/commands/ExampleCommand.java" << EOF
package $GROUP.$PLUGIN_DIR_NAME.commands;

import com.hypixel.hytale.server.core.command.Command;
import com.hypixel.hytale.server.core.command.CommandContext;
import com.hypixel.hytale.server.core.command.args.StringArg;

/**
 * Example command for $PLUGIN_NAME.
 * 
 * Usage: /example <message>
 */
public class ExampleCommand extends Command {
    
    public ExampleCommand() {
        super("example", "An example command for $PLUGIN_NAME");
        
        // Add command arguments
        addArg(StringArg.word("message"));
    }
    
    @Override
    public void execute(CommandContext ctx) {
        String message = ctx.get("message");
        ctx.sendMessage("You said: " + message);
    }
}
EOF

# Create example event listener
print_info "Creating example event listener..."
cat > "$PLUGIN_DIR/src/main/java/$PACKAGE_PATH/events/PlayerEventHandler.java" << EOF
package $GROUP.$PLUGIN_DIR_NAME.events;

import com.hypixel.hytale.server.core.event.player.PlayerConnectEvent;
import org.slf4j.Logger;

/**
 * Example event handler for player events.
 */
public class PlayerEventHandler {
    
    private final Logger logger;
    
    public PlayerEventHandler(Logger logger) {
        this.logger = logger;
    }
    
    /**
     * Called when a player connects to the server.
     */
    public void onPlayerConnect(PlayerConnectEvent event) {
        logger.info("Player connected: " + event.getPlayer().getName());
    }
}
EOF

# Create build.gradle
print_info "Creating build.gradle..."
cat > "$PLUGIN_DIR/build.gradle" << EOF
plugins {
    id 'java'
}

group = '$GROUP'
version = '$VERSION'

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
    // Add Hytale repository when available
    // maven { url 'https://repo.hytale.com/maven' }
}

dependencies {
    // Hytale Server API - compileOnly since it's provided at runtime
    compileOnly 'com.hypixel.hytale:hytale-server-api:1.0.0'
    
    // Annotations
    compileOnly 'com.google.code.findbugs:jsr305:3.0.2'
}

jar {
    // Include manifest.json and assets in the JAR root
    from('src/main/resources') {
        include 'manifest.json'
        include 'assets/**'
    }
    
    // Set JAR file name
    archiveBaseName.set('$PLUGIN_NAME')
    archiveVersion.set(version)
}

// Task to copy the built JAR to the mods folder
tasks.register('deploy', Copy) {
    dependsOn jar
    from jar.archiveFile
    into file('../server/mods')
}
EOF

# Create settings.gradle
print_info "Creating settings.gradle..."
cat > "$PLUGIN_DIR/settings.gradle" << EOF
rootProject.name = '$PLUGIN_DIR_NAME'
EOF

# Create .gitignore
print_info "Creating .gitignore..."
cat > "$PLUGIN_DIR/.gitignore" << EOF
# Gradle
.gradle/
build/
gradle/

# IDE
.idea/
*.iml
.vscode/
*.swp
*.swo
.project
.classpath
.settings/

# OS
.DS_Store
Thumbs.db

# Build outputs
*.jar
!gradle-wrapper.jar
out/
EOF

print_success "Plugin '$PLUGIN_NAME' created successfully!"
echo ""
echo -e "${GREEN}Plugin Structure:${NC}"
echo "$PLUGIN_DIR/"
echo "  src/main/java/$PACKAGE_PATH/"
echo "    $PLUGIN_NAME.java          (Main plugin class)"
echo "    commands/"
echo "      ExampleCommand.java      (Example command)"
echo "    events/"
echo "      PlayerEventHandler.java  (Example event handler)"
echo "    components/                (ECS components)"
echo "    systems/                   (ECS systems)"
echo "  src/main/resources/"
echo "    manifest.json              (Plugin manifest)"
echo "    assets/                    (Asset pack - optional)"
echo "  build.gradle"
echo "  settings.gradle"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. cd $PLUGIN_DIR"
echo "2. Edit manifest.json to add dependencies if needed"
echo "3. Implement your plugin logic in $PLUGIN_NAME.java"
echo "4. Build with: ./gradlew build"
echo "5. Deploy JAR to server's mods/ directory"
echo ""
