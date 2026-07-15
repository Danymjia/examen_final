import sys

filename = sys.argv[1]
counts = {}

with open(filename, 'r') as f:
    for line in f:
        parts = [p.strip() for p in line.strip().split(',') if p.strip()]
        if len(parts) >= 5:
            user, action, date, time, video = parts[0], parts[1], parts[2], parts[3], parts[4]
            hour = time.split(':')[0].zfill(2)
            
            counts[f"video:{video}:{action}"] = counts.get(f"video:{video}:{action}", 0) + 1
            counts[f"user:{user}"] = counts.get(f"user:{user}", 0) + 1
            counts[f"hour:{hour}"] = counts.get(f"hour:{hour}", 0) + 1

with open(f"{filename}.out", "w") as f:
    for k, v in counts.items():
        f.write(f"{k}\t{v}\n")
print(f"Mapper finalizo split: {filename}")
