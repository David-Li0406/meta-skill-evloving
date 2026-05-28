@echo off
setlocal enabledelayedexpansion

:: Hytale Plugin Scaffolding Script for Windows
:: Creates a basic Hytale server plugin project structure

title Hytale Plugin Scaffolding Tool

echo ======================================
echo    Hytale Plugin Scaffolding Tool
echo ======================================
echo.

:: Default values
set "DEFAULT_GROUP=com.example"
set "DEFAULT_VERSION=1.0.0"
set "DEFAULT_AUTHOR=Author"

:: Get plugin name
if "%~1"=="" (
    set /p "PLUGIN_NAME=Plugin Name (e.g., MyAwesomePlugin): "
) else (
    set "PLUGIN_NAME=%~1"
)

if "%PLUGIN_NAME%"=="" (
    echo [ERROR] Plugin name is required!
    exit /b 1
)

:: Basic validation - check first character is a letter
set "FIRST_CHAR=%PLUGIN_NAME:~0,1%"
echo %FIRST_CHAR%| findstr /r "[a-zA-Z]" >nul
if errorlevel 1 (
    echo [ERROR] Plugin name must start with a letter.
    exit /b 1
)

:: Get group/package
if "%~2"=="" (
    set /p "GROUP=Group/Package (default: %DEFAULT_GROUP%): "
    if "!GROUP!"=="" set "GROUP=%DEFAULT_GROUP%"
) else (
    set "GROUP=%~2"
)

:: Get version
if "%~3"=="" (
    set /p "VERSION=Version (default: %DEFAULT_VERSION%): "
    if "!VERSION!"=="" set "VERSION=%DEFAULT_VERSION%"
) else (
    set "VERSION=%~3"
)

:: Get author name
if "%~4"=="" (
    set /p "AUTHOR=Author Name (default: %DEFAULT_AUTHOR%): "
    if "!AUTHOR!"=="" set "AUTHOR=%DEFAULT_AUTHOR%"
) else (
    set "AUTHOR=%~4"
)

:: Get description
if "%~5"=="" (
    set /p "DESCRIPTION=Description (optional): "
) else (
    set "DESCRIPTION=%~5"
)

:: Convert plugin name to lowercase for directory
set "PLUGIN_DIR_NAME=%PLUGIN_NAME%"
call :ToLower PLUGIN_DIR_NAME
set "PLUGIN_DIR=%PLUGIN_DIR_NAME%"

:: Convert group to directory path (replace . with \)
set "PACKAGE_PATH=%GROUP%.%PLUGIN_DIR_NAME%"
set "PACKAGE_PATH=%PACKAGE_PATH:.=\%"

echo.
echo [INFO] Creating plugin: %PLUGIN_NAME%
echo [INFO] Location: .\%PLUGIN_DIR%
echo.

:: Check if directory already exists
if exist "%PLUGIN_DIR%" (
    echo [WARNING] Directory '%PLUGIN_DIR%' already exists!
    set /p "OVERWRITE=Overwrite? (y/N): "
    if /i not "!OVERWRITE!"=="y" (
        echo [INFO] Aborted.
        exit /b 0
    )
    rmdir /s /q "%PLUGIN_DIR%"
)

:: Create directory structure
echo [INFO] Creating directory structure...
mkdir "%PLUGIN_DIR%\src\main\java\%PACKAGE_PATH%\commands" 2>nul
mkdir "%PLUGIN_DIR%\src\main\java\%PACKAGE_PATH%\events" 2>nul
mkdir "%PLUGIN_DIR%\src\main\java\%PACKAGE_PATH%\components" 2>nul
mkdir "%PLUGIN_DIR%\src\main\java\%PACKAGE_PATH%\systems" 2>nul
mkdir "%PLUGIN_DIR%\src\main\resources\assets\Server\Content" 2>nul

:: Create package name for Java files
set "JAVA_PACKAGE=%GROUP%.%PLUGIN_DIR_NAME%"

:: Create manifest.json
echo [INFO] Creating manifest.json...
(
echo {
echo   "Group": "%GROUP%",
echo   "Name": "%PLUGIN_NAME%",
echo   "Version": "%VERSION%",
echo   "Description": "%DESCRIPTION%",
echo   "Authors": [
echo     {
echo       "Name": "%AUTHOR%"
echo     }
echo   ],
echo   "Main": "%JAVA_PACKAGE%.%PLUGIN_NAME%",
echo   "ServerVersion": "^>=1.0.0",
echo   "Dependencies": {},
echo   "OptionalDependencies": {},
echo   "DisabledByDefault": false,
echo   "IncludesAssetPack": false
echo }
) > "%PLUGIN_DIR%\src\main\resources\manifest.json"

:: Create main plugin class
echo [INFO] Creating main plugin class...
(
echo package %JAVA_PACKAGE%;
echo.
echo import com.hypixel.hytale.server.core.plugin.JavaPlugin;
echo import com.hypixel.hytale.server.core.plugin.JavaPluginInit;
echo import javax.annotation.Nonnull;
echo.
echo /**
echo  * Main plugin class for %PLUGIN_NAME%.
echo  * 
echo  * Lifecycle:
echo  * - setup^(^): Called after config load. Register commands, events, components here.
echo  * - start^(^): Called after all plugins complete setup. Safe to interact with other plugins.
echo  * - shutdown^(^): Called before disable. Cleanup resources here.
echo  */
echo public class %PLUGIN_NAME% extends JavaPlugin {
echo.    
echo     public %PLUGIN_NAME%^(@Nonnull JavaPluginInit init^) {
echo         super^(init^);
echo     }
echo.    
echo     @Override
echo     protected void setup^(^) {
echo         // Register commands, events, components, and systems here
echo         // Example: getCommandRegistry^(^).registerCommand^(new MyCommand^(^)^);
echo         // Example: getEventRegistry^(^).registerGlobal^(PlayerConnectEvent.class, this::onPlayerConnect^);
echo.        
echo         getLogger^(^).info^("%PLUGIN_NAME% setup complete!"^);
echo     }
echo.    
echo     @Override
echo     protected void start^(^) {
echo         // Called after all plugins complete setup
echo         // Safe to interact with world, players, and other plugins here
echo.        
echo         getLogger^(^).info^("%PLUGIN_NAME% started!"^);
echo     }
echo.    
echo     @Override
echo     protected void shutdown^(^) {
echo         // Cleanup resources, save data, cancel tasks here
echo.        
echo         getLogger^(^).info^("%PLUGIN_NAME% shutting down!"^);
echo     }
echo }
) > "%PLUGIN_DIR%\src\main\java\%PACKAGE_PATH%\%PLUGIN_NAME%.java"

:: Create example command class
echo [INFO] Creating example command...
(
echo package %JAVA_PACKAGE%.commands;
echo.
echo import com.hypixel.hytale.server.core.command.Command;
echo import com.hypixel.hytale.server.core.command.CommandContext;
echo import com.hypixel.hytale.server.core.command.args.StringArg;
echo.
echo /**
echo  * Example command for %PLUGIN_NAME%.
echo  * 
echo  * Usage: /example ^<message^>
echo  */
echo public class ExampleCommand extends Command {
echo.    
echo     public ExampleCommand^(^) {
echo         super^("example", "An example command for %PLUGIN_NAME%"^);
echo.        
echo         // Add command arguments
echo         addArg^(StringArg.word^("message"^)^);
echo     }
echo.    
echo     @Override
echo     public void execute^(CommandContext ctx^) {
echo         String message = ctx.get^("message"^);
echo         ctx.sendMessage^("You said: " + message^);
echo     }
echo }
) > "%PLUGIN_DIR%\src\main\java\%PACKAGE_PATH%\commands\ExampleCommand.java"

:: Create example event listener
echo [INFO] Creating example event listener...
(
echo package %JAVA_PACKAGE%.events;
echo.
echo import com.hypixel.hytale.server.core.event.player.PlayerConnectEvent;
echo import org.slf4j.Logger;
echo.
echo /**
echo  * Example event handler for player events.
echo  */
echo public class PlayerEventHandler {
echo.    
echo     private final Logger logger;
echo.    
echo     public PlayerEventHandler^(Logger logger^) {
echo         this.logger = logger;
echo     }
echo.    
echo     /**
echo      * Called when a player connects to the server.
echo      */
echo     public void onPlayerConnect^(PlayerConnectEvent event^) {
echo         logger.info^("Player connected: " + event.getPlayer^(^).getName^(^)^);
echo     }
echo }
) > "%PLUGIN_DIR%\src\main\java\%PACKAGE_PATH%\events\PlayerEventHandler.java"

:: Create build.gradle
echo [INFO] Creating build.gradle...
(
echo plugins {
echo     id 'java'
echo }
echo.
echo group = '%GROUP%'
echo version = '%VERSION%'
echo.
echo java {
echo     sourceCompatibility = JavaVersion.VERSION_21
echo     targetCompatibility = JavaVersion.VERSION_21
echo }
echo.
echo repositories {
echo     mavenCentral^(^)
echo     // Add Hytale repository when available
echo     // maven { url 'https://repo.hytale.com/maven' }
echo }
echo.
echo dependencies {
echo     // Hytale Server API - compileOnly since it's provided at runtime
echo     compileOnly 'com.hypixel.hytale:hytale-server-api:1.0.0'
echo.    
echo     // Annotations
echo     compileOnly 'com.google.code.findbugs:jsr305:3.0.2'
echo }
echo.
echo jar {
echo     // Include manifest.json and assets in the JAR root
echo     from^('src/main/resources'^) {
echo         include 'manifest.json'
echo         include 'assets/**'
echo     }
echo.    
echo     // Set JAR file name
echo     archiveBaseName.set^('%PLUGIN_NAME%'^)
echo     archiveVersion.set^(version^)
echo }
echo.
echo // Task to copy the built JAR to the mods folder
echo tasks.register^('deploy', Copy^) {
echo     dependsOn jar
echo     from jar.archiveFile
echo     into file^('../server/mods'^)
echo }
) > "%PLUGIN_DIR%\build.gradle"

:: Create settings.gradle
echo [INFO] Creating settings.gradle...
(
echo rootProject.name = '%PLUGIN_DIR_NAME%'
) > "%PLUGIN_DIR%\settings.gradle"

:: Create .gitignore
echo [INFO] Creating .gitignore...
(
echo # Gradle
echo .gradle/
echo build/
echo gradle/
echo.
echo # IDE
echo .idea/
echo *.iml
echo .vscode/
echo *.swp
echo *.swo
echo .project
echo .classpath
echo .settings/
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Build outputs
echo *.jar
echo ^!gradle-wrapper.jar
echo out/
) > "%PLUGIN_DIR%\.gitignore"

echo.
echo [SUCCESS] Plugin '%PLUGIN_NAME%' created successfully!
echo.
echo Plugin Structure:
echo %PLUGIN_DIR%\
echo   src\main\java\%PACKAGE_PATH%\
echo     %PLUGIN_NAME%.java          (Main plugin class)
echo     commands\
echo       ExampleCommand.java       (Example command)
echo     events\
echo       PlayerEventHandler.java   (Example event handler)
echo     components\                 (ECS components)
echo     systems\                    (ECS systems)
echo   src\main\resources\
echo     manifest.json               (Plugin manifest)
echo     assets\                     (Asset pack - optional)
echo   build.gradle
echo   settings.gradle
echo.
echo Next Steps:
echo 1. cd %PLUGIN_DIR%
echo 2. Edit manifest.json to add dependencies if needed
echo 3. Implement your plugin logic in %PLUGIN_NAME%.java
echo 4. Build with: gradlew build
echo 5. Deploy JAR to server's mods\ directory
echo.

endlocal
exit /b 0

:: Function to convert string to lowercase
:ToLower
for %%i in ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") do call set "%1=%%%1:%%~i%%"
goto :eof
