import os
import json
from collections import Counter, defaultdict

splits_dir = "/app/splits"
final_counts = Counter()

# Read all mapper output files
for file in os.listdir(splits_dir):
    if file.endswith(".out"):
        file_path = os.path.join(splits_dir, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) == 2:
                    key, count = parts[0], int(parts[1])
                    final_counts[key] += count

# Aggregate counts
video_actions = defaultdict(lambda: Counter())
user_counts = Counter()
hour_counts = Counter()

for key, count in final_counts.items():
    if key.startswith("video:"):
        _, name, action = key.split(':')
        video_actions[name][action] += count
    elif key.startswith("user:"):
        _, name = key.split(':')
        user_counts[name] += count
    elif key.startswith("hour:"):
        _, hour = key.split(':')
        hour_counts[hour] += count

# Calculate metrics
video_mas_visto = {"video": "N/A", "count": 0}
video_mas_likes = {"video": "N/A", "count": 0}
video_mas_comentado = {"video": "N/A", "count": 0}
video_max_ratio = {"video": "N/A", "ratio": 0.0, "views": 0, "interactions": 0}

for video, actions in video_actions.items():
    views = actions.get("view", 0)
    likes = actions.get("like", 0)
    comments = actions.get("comment", 0)
    shares = actions.get("shared", 0)
    
    if views > video_mas_visto["count"]:
        video_mas_visto = {"video": video, "count": views}
        
    if likes > video_mas_likes["count"]:
        video_mas_likes = {"video": video, "count": likes}
        
    if comments > video_mas_comentado["count"]:
        video_mas_comentado = {"video": video, "count": comments}
        
    if views > 0:
        ratio = (likes + comments + shares) / views
        if ratio > video_max_ratio["ratio"]:
            video_max_ratio = {
                "video": video,
                "ratio": ratio,
                "views": views,
                "interactions": likes + comments + shares
            }

usuario_mas_recurrente = {"usuario": "N/A", "count": 0}
if user_counts:
    user, count = user_counts.most_common(1)[0]
    usuario_mas_recurrente = {"usuario": user, "count": count}

hora_mas_interaccion = {"hora": "N/A", "count": 0}
if hour_counts:
    hour, count = hour_counts.most_common(1)[0]
    hora_mas_interaccion = {"hora": hour, "count": count}

results = {
    "video_mas_visto": video_mas_visto,
    "video_mas_likes": video_mas_likes,
    "video_mas_comentado": video_mas_comentado,
    "usuario_mas_recurrente": usuario_mas_recurrente,
    "hora_mas_interaccion": hora_mas_interaccion,
    "video_max_ratio": video_max_ratio
}

# Print results to stdout
print("\n" + "="*40, flush=True)
print("   RESULTADOS DEL PROCESAMIENTO MAPREDUCE", flush=True)
print("="*40, flush=True)
print(f"Video más visto: {video_mas_visto['video']} ({video_mas_visto['count']} views)", flush=True)
print(f"Video con más likes: {video_mas_likes['video']} ({video_mas_likes['count']} likes)", flush=True)
print(f"Video más comentado: {video_mas_comentado['video']} ({video_mas_comentado['count']} comments)", flush=True)
print(f"Usuario más recurrente: {usuario_mas_recurrente['usuario']} ({usuario_mas_recurrente['count']} interactions)", flush=True)
print(f"Hora con más interacción: {hora_mas_interaccion['hora']}:00 ({hora_mas_interaccion['count']} interactions)", flush=True)
print(f"Video con mayor Ratio de Interacción: {video_max_ratio['video']} (Ratio: {video_max_ratio['ratio']:.4f})", flush=True)
print("="*40 + "\n", flush=True)

# Save to shared JSON file
results_path = "/app/resultados.json"
with open(results_path, 'w', encoding='utf-8') as rf:
    json.dump(results, rf, indent=4)

# Save to shared TXT file
with open("/app/resultados.txt", 'w', encoding='utf-8') as tf:
    tf.write("RESULTADOS DEL PROCESAMIENTO MAPREDUCE\n")
    tf.write("="*40 + "\n")
    tf.write(f"Video más visto: {video_mas_visto['video']} ({video_mas_visto['count']} views)\n")
    tf.write(f"Video con más likes: {video_mas_likes['video']} ({video_mas_likes['count']} likes)\n")
    tf.write(f"Video más comentado: {video_mas_comentado['video']} ({video_mas_comentado['count']} comments)\n")
    tf.write(f"Usuario más recurrente: {usuario_mas_recurrente['usuario']} ({usuario_mas_recurrente['count']} interactions)\n")
    tf.write(f"Hora con más interacción: {hora_mas_interaccion['hora']}:00 ({hora_mas_interaccion['count']} interactions)\n")
    tf.write(f"Video con mayor Ratio de Interacción: {video_max_ratio['video']} (Ratio: {video_max_ratio['ratio']:.4f})\n")
    tf.write("="*40 + "\n")

print("Reducer finished and saved metrics to /app/resultados.json and /app/resultados.txt", flush=True)
