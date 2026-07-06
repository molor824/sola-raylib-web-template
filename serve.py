import re
import shutil
import subprocess
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer

PATTERN = r'name\s*=\s*"([^"]+)"'
PORT = 3000

TOML = "Cargo.toml"

project_name = "raylib-web"

with open(TOML) as f:
    match = re.search(PATTERN, f.read())
    if match:
        project_name = match.group(1)
        print(f"Detected project name: {project_name}")
    else:
        print(f"Failed to detect project name, using default: {project_name}")

JS_FILENAME = f"{project_name}.js"
WASM_FILENAME = f"{project_name.replace('-', '_')}.wasm"

SRC_DIR = Path("target/wasm32-unknown-emscripten/release")
DST_DIR = Path(".static")

JS_SRC_PATH = SRC_DIR / JS_FILENAME
WASM_SRC_PATH = SRC_DIR / WASM_FILENAME

JS_DST_PATH = DST_DIR / "index.js"
WASM_DST_PATH = DST_DIR / WASM_FILENAME

subprocess.run(["cargo", "build", "--release", "--target=wasm32-unknown-emscripten"])

DST_DIR.mkdir(parents=True, exist_ok=True)

total_size = Path("index.html").stat().st_size


def try_copy(src, dst):
    global total_size
    print(f"Copying {src} to {dst}: ", end="")
    try:
        shutil.copy(src, dst)
        total_size += dst.stat().st_size
        print("OK")
    except OSError as err:
        print(err)


try_copy(JS_SRC_PATH, JS_DST_PATH)
try_copy(WASM_SRC_PATH, WASM_DST_PATH)

mib = 1024 * 1024
print(f"Total size: {total_size / mib:.2f}MiB")

if total_size >= (64 * mib):
    print(f"Project size overflowed! {total_size} >= {64 * mib}")

with TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Server started on port: {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
