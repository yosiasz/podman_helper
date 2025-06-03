influxdb3.exe serve --node-id node01 --object-store=file --data-dir ./influxdb-data

Authorization: Bearer apiv3_O5FcCw2pwT-uaSqsJeW3c4Bow6LBpWULLfiYgvpuOEsgmkjLF5ju6WXiCYbWfjZcqnvYC7Rba-ZX11M0DyG7PQ

.\influxdb3.exe write --database boombap --token Authorization: Bearer apiv3_O5FcCw2pwT-uaSqsJeW3c4Bow6LBpWULLfiYgvpuOEsgmkjLF5ju6WXiCYbWfjZcqnvYC7Rba-ZX11M0DyG7PQ --precision ns --accept-partial 'cpu,host=Alpha,region=us-west,application=webserver val=1i,usage_percent=20.5,status="OK"
cpu,host=Bravo,region=us-east,application=database val=2i,usage_percent=55.2,status="OK"
cpu,host=Charlie,region=us-west,application=cache val=3i,usage_percent=65.4,status="OK"
cpu,host=Bravo,region=us-east,application=database val=4i,usage_percent=70.1,status="Warn"
cpu,host=Bravo,region=us-central,application=database val=5i,usage_percent=80.5,status="OK"
cpu,host=Alpha,region=us-west,application=webserver val=6i,usage_percent=25.3,status="Warn"'
