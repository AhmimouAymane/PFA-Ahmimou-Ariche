@echo off
echo ========================================
echo Creating Database: chatbot_admin
echo ========================================
echo.

REM Try to create database using Python script
cd backend\scripts
echo Creating database using Python script...
python create_db_simple.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Database setup completed!
    echo.
    echo You can now continue with the backend setup.
) else (
    echo.
    echo ✗ Failed to create database.
    echo.
    echo Alternative methods:
    echo 1. Use MySQL Workbench or command line client
    echo 2. Run: CREATE DATABASE chatbot_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    echo 3. Make sure MySQL service is running
)

cd ..\..
pause
