import urllib.request
import os

print("Descargando datos...")
data = urllib.request.urlopen("http://nginx/datos").read().decode('utf-8')

with open("datos.txt", "w") as f:
    f.write(data)

lines = [l.strip() for l in data.strip().split('\n') if l.strip()]
os.makedirs("splits", exist_ok=True)

# Limpiar antiguos
for f in os.listdir("splits"):
    if f.endswith(".txt") or f.endswith(".out"):
        os.remove(os.path.join("splits", f))

chunk_size = 100
for i in range(0, len(lines), chunk_size):
    chunk = lines[i:i+chunk_size]
    with open(f"splits/part_{i//chunk_size:02d}.txt", "w") as f:
        f.write("\n".join(chunk))
print("Datos divididos en splits.")
