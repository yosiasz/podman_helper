unable to download windows emulator docker image

unable to pull windows emulator
use linux emulator

curl -k https://localhost:8081/\_explorer/emulator.pem > ~/emulatorcert.crt

Import-Certificate -FilePath C:\podman\cosmos\emulatorcert.crt -CertStoreLocation Cert:\LocalMachine\Root

podman run --name azure-cosmosdb-emulator --memory 2GB --mount "type=bind,source=/mnt/c/.podman_volumes/CosmosDBEmulator/bind-mount,destination=/usr/share/" --interactive --tty -p 8081:8081 -p 8900:8900 -p 8901:8901 -p 8902:8902 -p 10250:10250 -p 10251:10251 -p 10252:10252 -p 10253:10253 -p 10254:10254 -p 10255:10255 -p 10256:10256 -p 10350:10350 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator

REST API

https://h-savran.blogspot.com/2019/02/cosmos-db-rest-api-with-postman.html
