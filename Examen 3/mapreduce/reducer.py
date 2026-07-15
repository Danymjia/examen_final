import os
import json

counts = {}
for file in os.listdir("splits"):
    if file.endswith(".out"):
        with open(f"splits/{file}", "r") as f:
            for line in f:
                k, v = line.strip().split('\t')
                counts[k] = counts.get(k, 0) + int(v)

video_mas_visto = ["", 0]
video_mas_likes = ["", 0]
video_mas_comentado = ["", 0]
user_mas_recurrente = ["", 0]
hour_mas_interaccion = ["", 0]
video_stats = {}

for k, v in counts.items():
    parts = k.split(':')
    if parts[0] == "video":
        video, action = parts[1], parts[2]
        if action == "view" and v > video_mas_visto[1]:
            video_mas_visto = [video, v]
        if action == "like" and v > video_mas_likes[1]:
            video_mas_likes = [video, v]
        if action == "comment" and v > video_mas_comentado[1]:
            video_mas_comentado = [video, v]
            
        if video not in video_stats:
            video_stats[video] = {"view": 0, "like": 0, "comment": 0, "shared": 0}
        video_stats[video][action] = v
        
    elif parts[0] == "user" and v > user_mas_recurrente[1]:
        user_mas_recurrente = [parts[1], v]
    elif parts[0] == "hour" and v > hour_mas_interaccion[1]:
        hour_mas_interaccion = [parts[1], v]

video_max_ratio = ["", 0.0]
for video, stats in video_stats.items():
    views = stats["view"]
    if views > 0:
        ratio = (stats["like"] + stats["comment"] + stats["shared"]) / views
        if ratio > video_max_ratio[1]:
            video_max_ratio = [video, ratio]

results = {
    "video_mas_visto": {"video": video_mas_visto[0], "count": video_mas_visto[1]},
    "video_mas_likes": {"video": video_mas_likes[0], "count": video_mas_likes[1]},
    "video_mas_comentado": {"video": video_mas_comentado[0], "count": video_mas_comentado[1]},
    "usuario_mas_recurrente": {"usuario": user_mas_recurrente[0], "count": user_mas_recurrente[1]},
    "hora_mas_interaccion": {"hora": hour_mas_interaccion[0], "count": hour_mas_interaccion[1]},
    "video_max_ratio": {"video": video_max_ratio[0], "ratio": video_max_ratio[1]}
}

with open("resultados.json", "w") as f:
    json.dump(results, f, indent=4)

print("Resultados guardados en resultados.json")
