@echo off
echo Starting Aurora Kubernetes deployment...

REM Clean up existing deployment first
echo Cleaning up existing deployment...
call "%~dp0cleanup.bat"
if %errorlevel% neq 0 (
    echo Failed to clean up existing deployment
    exit /b %errorlevel%
)
timeout /t 5 /nobreak

REM Build Docker image
echo Building Docker image...

docker build -t krjaeh0/aurora:latest -f %~dp0..\Dockerfile %~dp0..
if %errorlevel% neq 0 (
    echo Failed to build Docker image
    exit /b %errorlevel%
)

REM Create Kind cluster
echo Creating Kind cluster...
cd Kubernetes
kind create cluster --config kind-config.yaml --name aurora-cluster
if %errorlevel% neq 0 (
    echo Failed to create Kind cluster
    exit /b %errorlevel%
)

REM Load Docker image to Kind
echo Loading Docker image to Kind cluster...
kind load docker-image krjaeh0/aurora:latest --name aurora-cluster
if %errorlevel% neq 0 (
    echo Failed to load Docker image to Kind cluster
    exit /b %errorlevel%
)

REM Deploy application
echo Deploying application...
kubectl apply -f aurora-deployment.yaml
if %errorlevel% neq 0 (
    echo Failed to deploy application
    exit /b %errorlevel%
)

echo.
echo Deployment completed successfully!
echo Waiting for pod to be ready...
timeout /t 10 /nobreak

REM Show deployment status
echo.
echo Deployment Status:
kubectl get pods -o wide
echo.
echo Service Status:
kubectl get services
echo.
echo You can access the service at http://localhost:30080
