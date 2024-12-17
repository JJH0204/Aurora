@echo off
echo Cleaning up Aurora Kubernetes deployment...

REM Find and kill process using port 30080
echo Checking for processes using port 30080...
set "found_pid="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :30080') do (
    if not defined found_pid (
        echo Terminating process with PID: %%a
        taskkill /F /PID %%a 2>nul
        set "found_pid=1"
    )
)

REM Delete Kind cluster
echo Deleting Kind cluster...
kind delete cluster --name aurora-cluster

REM Clean up Docker containers and images related to Kind (if any remain)
echo Cleaning up related Docker resources...
for /f "tokens=1" %%i in ('docker ps -a ^| findstr "aurora-cluster"') do (
    docker rm -f %%i
)

REM Optional: Clean up any remaining Docker images
for /f "tokens=3" %%i in ('docker images ^| findstr "aurora"') do (
    docker rmi -f %%i
)

echo.
echo Cleanup completed successfully!
