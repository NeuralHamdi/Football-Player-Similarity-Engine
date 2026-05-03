import kagglehub

# Download latest version
path = kagglehub.dataset_download("hubertsidorowicz/football-players-stats-2025-2026")

print("Path to dataset files:", path)