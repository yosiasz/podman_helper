@echo off
setlocal

rem === Create output directory ===
mkdir certs
cd certs

echo [INFO] Generating Root CA key and certificate...
C:\PROGRA~1\OPENSS~1\bin\openssl.exe genrsa -out ca-key.pem 2048
C:\PROGRA~1\OPENSS~1\bin\openssl.exe req -new -x509 -days 3650 -key ca-key.pem -out ca.pem -subj "/CN=MySQL CA"

echo [INFO] Generating server key and CSR...
C:\PROGRA~1\OPENSS~1\bin\openssl.exe genrsa -out server-key.pem 2048
C:\PROGRA~1\OPENSS~1\bin\openssl.exe req -new -key server-key.pem -out server.csr -config server-ext.cnf

echo [INFO] Signing server certificate with Root CA...
C:\PROGRA~1\OPENSS~1\bin\openssl.exe x509 -req -in server.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial ^
    -out server-cert.pem -days 3650 -extfile server-ext.cnf -extensions req_ext

echo [INFO] Generating client key and certificate...
C:\PROGRA~1\OPENSS~1\bin\openssl.exe genrsa -out client-key.pem 2048
C:\PROGRA~1\OPENSS~1\bin\openssl.exe req -new -key client-key.pem -out client.csr -subj "/CN=MySQL Client"
C:\PROGRA~1\OPENSS~1\bin\openssl.exe x509 -req -in client.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial ^
    -out client-cert.pem -days 3650

echo [INFO] Cleaning up...
del *.csr
del *.srl

echo [DONE] Certificates generated in certs\:
echo  - ca.pem (Root CA)
echo  - server-cert.pem / server-key.pem
echo  - client-cert.pem / client-key.pem

endlocal
