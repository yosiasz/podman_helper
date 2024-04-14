#Requires -RunAsAdministrator
#Requires -Version 7

Write-Information "Downloading certificate from local Cosmos DB Instance"
curl -k https://localhost:8081/_explorer/emulator.pem > $env:TEMP/emulator.crt

Write-Information "Adding certificate to certificate store"
Import-Certificate -FilePath $env:TEMP/emulator.crt -CertStoreLocation Cert:\LocalMachine\Root

Remove-Item $env:TEMP/emulator.crt