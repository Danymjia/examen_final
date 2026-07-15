import urllib.request
import os
import time

url = "http://nginx/datos"
output_file = "/app/datos.txt"
splits_dir = "/app/splits"

print("Preparador starting. Waiting for nginx and flask apps to be ready...", flush=True)

data = None
for i in range(15):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                data = response.read().decode('utf-8')
                print("Successfully fetched data from load balancer!", flush=True)
                break
    except Exception as e:
        print(f"Attempt {i+1} failed: {e}. Retrying in 3 seconds...", flush=True)
        time.sleep(3)

if not data:
    print("Error: Could not retrieve data from web server. Exiting.", flush=True)
    exit(1)

os.makedirs(splits_dir, exist_ok=True)
for f in os.listdir(splits_dir):
    file_path = os.path.join(splits_dir, f)
    if os.path.isfile(file_path):
        os.remove(file_path)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(data)

lines = [l for l in data.strip().split('\n') if l.strip()]
chunk_size = 100
num_splits = (len(lines) + chunk_size - 1) // chunk_size

for idx in range(num_splits):
    chunk = lines[idx * chunk_size : (idx + 1) * chunk_size]
    split_filename = f"{splits_dir}/part_{idx:02d}.txt"
    with open(split_filename, 'w', encoding='utf-8') as sf:
        sf.write('\n'.join(chunk) + '\n')
    print(f"Created split: {split_filename} with {len(chunk)} lines.", flush=True)

print("Preparador completed successfully!", flush=True)
