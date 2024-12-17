@echo off
echo Starting Security Monitoring Deployment...

REM Create necessary directories
mkdir %~dp0logs 2>nul

REM Label security nodes
echo Labeling nodes for security components...
kubectl label nodes --all node-type=security --overwrite

REM Deploy ELK Stack
echo Deploying ELK Stack...
kubectl apply -f %~dp0elk\elk-namespace.yaml
kubectl apply -f %~dp0elk\elasticsearch.yaml
kubectl apply -f %~dp0elk\kibana.yaml

REM Wait for Elasticsearch to be ready
echo Waiting for Elasticsearch to be ready...
:WAIT_ES
kubectl get pods -n elk-system | findstr "elasticsearch.*1/1.*Running"
if errorlevel 1 (
    echo Waiting for Elasticsearch pod...
    timeout /t 10 /nobreak > nul
    goto WAIT_ES
)
timeout /t 30 /nobreak

REM Wait for Kibana to be ready
echo Waiting for Kibana to be ready...
:WAIT_KIBANA
kubectl get pods -n elk-system | findstr "kibana.*1/1.*Running"
if errorlevel 1 (
    echo Waiting for Kibana pod...
    timeout /t 10 /nobreak > nul
    goto WAIT_KIBANA
)
timeout /t 10 /nobreak

REM Create Elasticsearch credentials
echo Creating Elasticsearch credentials...
kubectl apply -f %~dp0monitoring\elasticsearch-secret.yaml

REM Deploy monitoring components
echo Deploying monitoring components...
kubectl apply -f %~dp0monitoring\monitoring-namespace.yaml
kubectl apply -f %~dp0monitoring\suricata-config.yaml
kubectl apply -f %~dp0monitoring\suricata-daemonset.yaml
kubectl apply -f %~dp0monitoring\filebeat-config.yaml
kubectl apply -f %~dp0monitoring\filebeat-daemonset.yaml

REM Wait for monitoring components to be ready
echo Waiting for monitoring components to be ready...
:WAIT_MONITORING
kubectl get pods -n monitoring | findstr "suricata.*1/1.*Running" | findstr "filebeat.*1/1.*Running"
if errorlevel 1 (
    echo Waiting for monitoring pods...
    timeout /t 10 /nobreak > nul
    goto WAIT_MONITORING
)

REM Show deployment status
echo.
echo Deployment Status:
echo ELK Stack:
kubectl get pods -n elk-system
echo.
echo Monitoring Components:
kubectl get pods -n monitoring
echo.
echo Services:
kubectl get services -n elk-system
echo.
echo Kibana will be available at http://localhost:30601
echo Default credentials:
echo Username: elastic
echo Password: choa0306@@

echo.
echo Security monitoring deployment completed successfully!
