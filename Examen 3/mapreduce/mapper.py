import sys
from collections import Counter

if len(sys.argv) < 2:
    print("Usage: python mapper.py <filename>", file=sys.stderr)
    sys.exit(1)

filename = sys.argv[1]
counts = Counter()

with open(filename, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 5:
            # Format: usuario, accion, fecha, hora, short
            usuario, accion, fecha, hora, short = parts[0], parts[1], parts[2], parts[3], parts[4]
            
            # Map video actions
            counts[f"video:{short}:{accion}"] += 1
            
            # Map user interactions
            counts[f"user:{usuario}"] += 1
            
            # Map hour of day
            hour_part = hora.split(':')[0]
            try:
                hour_formatted = f"{int(hour_part):02d}"
                counts[f"hour:{hour_formatted}"] += 1
            except ValueError:
                pass

# Write results to filename.out
out_filename = f"{filename}.out"
with open(out_filename, 'w', encoding='utf-8') as out:
    for key, count in counts.items():
        out.write(f"{key}\t{count}\n")

print(f"Mapper finished processing {filename}. Created {out_filename}", flush=True)
