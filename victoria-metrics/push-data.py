import requests
import time
import random

VM_URL = "http://localhost:8428/api/v1/import/prometheus"

while True:
    cpu_usage = random.uniform(0, 100)
    mem_usage = random.uniform(0, 16000)

    data = f"""
    cpu_usage_percent{{instance="server1"}} {cpu_usage}
    memory_usage_megabytes{{instance="server1"}} {mem_usage}
    """

    response = requests.post(VM_URL, data=data)

    if response.status_code in (200, 204):
        print(f"✅ Pushed: CPU={cpu_usage:.2f}% MEM={mem_usage:.2f}MB")
    else:
        print(f"❌ Error: {response.status_code} {response.text}")

    time.sleep(5)
