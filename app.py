from flask import Flask
import os

app = Flask(__name__)

# data directory (inside container this will be /app/data when WORKDIR=/app)
DATA_DIR = os.path.join(os.getcwd(), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

VISITS_FILE = os.path.join(DATA_DIR, "visits.txt")

def read_count():
    if not os.path.exists(VISITS_FILE):
        with open(VISITS_FILE, "w") as f:
            f.write("0")
    with open(VISITS_FILE, "r") as f:
        s = f.read().strip()
    try:
        return int(s)
    except:
        return 0

def write_count(n):
    with open(VISITS_FILE, "w") as f:
        f.write(str(n))

@app.route("/")
def index():
    n = read_count() + 1
    write_count(n)
    return f"""<!DOCTYPE html>
<html>
<head><title>Hello Volume</title></head>
<body>
  <h1>Hello — you are visitor #{n}!</h1>
  <p>The visit count is stored in a Docker volume (or a host folder if you bind-mount).</p>
</body>
</html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
