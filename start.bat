@echo off
setlocal enabledelayedexpansion
title Tooling Master Records Management

:: IMPORTANT: Change to the directory where this batch file is located
cd /d "%~dp0"

echo ============================================
echo   Tooling Master Records Management
echo   One-Click Setup and Run
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    pause
    exit /b 1
)
echo [OK] Python found.

:: Start PostgreSQL service if not running
echo [CHECK] Starting PostgreSQL...
:: Try all common PostgreSQL service names
net start postgresql-x64-17 >nul 2>&1
net start postgresql-x64-16 >nul 2>&1
net start postgresql-x64-15 >nul 2>&1
net start postgresql-x64-14 >nul 2>&1
net start postgresql-x64-13 >nul 2>&1
net start postgresql >nul 2>&1
:: Also try to find dynamically
for /f "tokens=2" %%s in ('sc query state^= all ^| findstr /i "SERVICE_NAME.*ostgre"') do (
    net start %%s >nul 2>&1
)

:: Wait a moment for PostgreSQL to be ready
timeout /t 3 /nobreak >nul

:: Verify PostgreSQL is actually reachable on port 5432
powershell -Command "try { $c = New-Object System.Net.Sockets.TcpClient('localhost', 5433); $c.Close(); exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] PostgreSQL is NOT running on port 5433!
    echo.
    echo Please do ONE of the following:
    echo.
    echo   Option 1: Install PostgreSQL
    echo     Download from: https://www.postgresql.org/download/windows/
    echo     During install, keep default port 5432 and remember your password.
    echo     Make sure "Run as service" is checked.
    echo.
    echo   Option 2: Start PostgreSQL manually
    echo     1. Press Win+R, type services.msc, press Enter
    echo     2. Find any service with "postgres" in the name
    echo     3. Right-click it and choose "Start"
    echo     4. Then re-run this script
    echo.
    pause
    exit /b 1
)
echo [OK] PostgreSQL is running.

:: Ask for PostgreSQL password
echo.
set /p DB_PASS="Enter your PostgreSQL password: "
echo.

:: Write .env file with the password
echo DATABASE_URL=postgresql://postgres:%DB_PASS%@localhost:5433/tooling_db> .env
echo DEBUG=false>> .env
echo [OK] Password saved to .env

:: Also update alembic.ini
powershell -Command "(Get-Content '%~dp0alembic.ini') -replace 'sqlalchemy.url = .*', 'sqlalchemy.url = postgresql://postgres:%DB_PASS%@localhost:5433/tooling_db' | Set-Content '%~dp0alembic.ini'"
echo [OK] alembic.ini updated.

:: Create virtual environment first (needed for DB creation)
if not exist "venv\Scripts\python.exe" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)

:: Install psycopg2 early for DB creation
venv\Scripts\python.exe -m pip install psycopg2-binary -q 2>nul

:: Create database using Python (avoids psql.exe DLL issues)
echo [SETUP] Creating database if not exists...
venv\Scripts\python.exe -c "import psycopg2; from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT; conn=psycopg2.connect(host='localhost',port=5433,user='postgres',password='%DB_PASS%'); conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT); cur=conn.cursor(); cur.execute(\"SELECT 1 FROM pg_database WHERE datname='tooling_db'\"); exists=cur.fetchone(); cur.execute('CREATE DATABASE tooling_db') if not exists else None; conn.close(); print('[OK] Database ready.' if not exists else '[OK] Database already exists.')"
if %errorlevel% neq 0 (
    echo [WARNING] Could not create database. Check if PostgreSQL is running and password is correct.
)

:: Install dependencies
echo [SETUP] Installing dependencies...
venv\Scripts\python.exe -m pip install -r requirements.txt -q 2>nul
venv\Scripts\python.exe -m pip install aiofiles -q 2>nul
echo [OK] Dependencies installed.

:: Run database migrations
echo [SETUP] Running database migrations...
venv\Scripts\python.exe -m alembic upgrade head
if %errorlevel% neq 0 (
    echo [INFO] Migration failed - recreating database from scratch...
    venv\Scripts\python.exe -c "import psycopg2; from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT; conn=psycopg2.connect(host='localhost',port=5433,user='postgres',password='%DB_PASS%'); conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT); cur=conn.cursor(); cur.execute('DROP DATABASE IF EXISTS tooling_db'); cur.execute('CREATE DATABASE tooling_db'); conn.close(); print('[OK] Database recreated.')"
    venv\Scripts\python.exe -m alembic upgrade head
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Database migration failed!
        echo.
        echo Possible issues:
        echo   1. PostgreSQL is not running (start it from Services)
        echo   2. Wrong password entered
        echo.
        echo Then re-run this script.
        pause
        exit /b 1
    )
)
echo [OK] Database ready.

:: Start the server
echo.
echo ============================================
echo   Server is running!
echo   UI:   http://localhost:8000/ui
echo   API:  http://localhost:8000/docs
echo ============================================
echo.
echo Press Ctrl+C to stop the server.
echo.

:: Open browser automatically
start http://localhost:8000/ui

:: Run uvicorn
venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000

pause
