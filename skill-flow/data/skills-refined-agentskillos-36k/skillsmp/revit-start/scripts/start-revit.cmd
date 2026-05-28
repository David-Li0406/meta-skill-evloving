@echo off
setlocal enabledelayedexpansion

if "%~1"=="" (
  echo Usage: launch-revit.cmd ^<2021^|2023^|2024^|2026^>
  exit /b 1
)

set "VERSION=%~1"
set "EXE="
set "TEMPLATE="

rem Ensure Revit is not running before editing settings
tasklist /fi "IMAGENAME eq Revit.exe" | find /i "Revit.exe" >nul 2>&1
if not errorlevel 1 (
  echo Revit is currently running. Close it before proceeding.
  exit /b 1
)

if /i "%VERSION%"=="2021" set "EXE=C:\Program Files\Autodesk\Revit 2021\Revit.exe"
if /i "%VERSION%"=="2023" set "EXE=C:\Program Files\Autodesk\Revit 2023\Revit.exe"
if /i "%VERSION%"=="2024" set "EXE=C:\Program Files\Autodesk\Revit 2024\Revit.exe"
if /i "%VERSION%"=="2026" set "EXE=C:\Program Files\Autodesk\Revit 2026\Revit.exe"

if "%EXE%"=="" (
  echo Invalid version: %VERSION%
  exit /b 1
)

if /i "%VERSION%"=="2024" (
  for %%F in ("%~dp0..\assets\2024templaterevitskill.rte") do set "TEMPLATE=%%~fF"
)

set "INI=%APPDATA%\Autodesk\Revit\Autodesk Revit %VERSION%\Revit.ini"
if exist "%INI%" (
  set "TMP=%TEMP%\Revit-%VERSION%-clean.ini"
  if exist "%TMP%" del /f /q "%TMP%" >nul 2>&1
  set "SKIP=0"
  for /f "usebackq delims=" %%L in ("%INI%") do (
    set "LINE=%%L"
    if /i "!LINE!"=="[Recent File List]" (
      echo [Recent File List]>>"%TMP%"
      set "SKIP=1"
    ) else (
      if "!LINE:~0,1!"=="[" (
        if "!SKIP!"=="1" set "SKIP=0"
      )
      if "!SKIP!"=="0" echo(!LINE!>>"%TMP%"
    )
  )
  if exist "%TMP%" (
    copy /y "%TMP%" "%INI%" >nul 2>&1
    del /f /q "%TMP%" >nul 2>&1
  )
)

if not exist "%EXE%" (
  for /f "delims=" %%F in ('dir /b /s "C:\Program Files\Autodesk\Revit %VERSION%\Revit.exe" 2^>nul') do (
    set "EXE=%%F"
    goto :found
  )
)

:found
if not exist "%EXE%" (
  echo Revit %VERSION% not found. Expected at: C:\Program Files\Autodesk\Revit %VERSION%\Revit.exe
  exit /b 1
)

if defined TEMPLATE (
  if not exist "%TEMPLATE%" (
    echo Revit %VERSION% template not found: "%TEMPLATE%"
    exit /b 1
  )
  echo Launching Revit %VERSION%: "%EXE%" "%TEMPLATE%" /nosplash
  start "" /MAX /REALTIME "%EXE%" "%TEMPLATE%" /nosplash
) else (
  echo Launching Revit %VERSION%: "%EXE%" /nosplash
  start "" /MAX /REALTIME "%EXE%" /nosplash
)
endlocal
