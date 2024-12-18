@echo off

kubectl get pods -l app^=aurora --no-headers -o custom-columns^=":metadata.name" > temp.txt
set /p NGINX_POD=<temp.txt
del temp.txt

echo Pod name: %NGINX_POD%

if "%NGINX_POD%"=="" (
    echo No NGINX pod found.
    exit /b 1
)

kubectl exec %NGINX_POD% -- nginx -s reload