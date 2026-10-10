import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
import time
import subprocess
import signal
import socket
import webbrowser
import threading
import http.server
import socketserver
import urllib.request

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_DIR, "backend")

processes = []
redirect_server = None

def print_banner():
    print("\033[96m" + "=" * 78)
    print("      CONTRACTMIND v1.5 - AUTONOMOUS LEGAL AI STUDIO (ALPINE CORE)")
    print("            AI Builders Congress 2026 - Track: JusticeSphere_AI")
    print("=" * 78 + "\033[0m\n")

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def free_port(port):
    """Frees port if an old zombie process is holding it."""
    if sys.platform == "win32":
        try:
            output = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True).decode()
            for line in output.strip().split('\n'):
                parts = line.strip().split()
                if len(parts) >= 5 and 'LISTENING' in parts:
                    pid = parts[-1]
                    if pid != str(os.getpid()):
                        subprocess.call(['taskkill', '/F', '/PID', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def start_port_3000_redirector():
    """Lightweight HTTP server on port 3000 forwarding to port 8000."""
    class RedirectHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(302)
            self.send_header('Location', f'http://localhost:8000{self.path}')
            self.end_headers()
        def log_message(self, format, *args):
            pass # Suppress noisy logs

    def run():
        global redirect_server
        try:
            socketserver.TCPServer.allow_reuse_address = True
            with socketserver.TCPServer(('127.0.0.1', 3000), RedirectHandler) as httpd:
                redirect_server = httpd
                httpd.serve_forever()
        except Exception:
            pass

    t = threading.Thread(target=run, daemon=True)
    t.start()

def wait_for_service(url, name, timeout=25):
    print(f"[*] Waiting for {name} to become ready at {url}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'HealthCheck'})
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status in (200, 304):
                    print(f"\033[92m[✓] {name} is ONLINE and healthy!\033[0m")
                    return True
        except Exception:
            time.sleep(1)
    print(f"\033[93m[!] Warning: {name} did not answer health probe within {timeout}s, but continuing...\033[0m")
    return False

def cleanup(sig=None, frame=None):
    print("\n\n\033[93m[*] Shutting down ContractMind v1.5 services...\033[0m")
    if redirect_server:
        try:
            redirect_server.shutdown()
        except Exception:
            pass
    for p in processes:
        try:
            if sys.platform == "win32":
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                p.terminate()
        except Exception:
            pass
    print("\033[92m[✓] All services stopped cleanly. Goodbye!\033[0m")
    sys.exit(0)

def main():
    print_banner()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # 1. Clean ports
    free_port(8000)
    free_port(3000)

    # 2. Start Port 3000 Forwarder (seamless transition from old React port to port 8000)
    start_port_3000_redirector()

    # 3. Start Unified Legal Engine & Alpine.js Studio on Port 8000
    print("[*] Starting Python FastAPI Legal Engine & Alpine.js Studio on Port 8000...")
    log_file_path = os.path.join(BACKEND_DIR, "backend.log")
    try:
        backend_log_file = open(log_file_path, "w", encoding="utf-8", errors="replace")
    except Exception:
        backend_log_file = subprocess.DEVNULL

    backend_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=BACKEND_DIR,
        stdout=backend_log_file,
        stderr=subprocess.STDOUT
    )
    processes.append(backend_proc)

    # 4. Wait for health check
    backend_ready = wait_for_service("http://127.0.0.1:8000/health", "ContractMind v1.5 Studio (Port 8000)")
    if not backend_ready and os.path.exists(log_file_path):
        try:
            with open(log_file_path, "r", encoding="utf-8", errors="replace") as f:
                recent_logs = "".join(f.readlines()[-25:])
                if recent_logs.strip():
                    print(f"\033[91m[!] Backend Startup Log Output:\n{recent_logs}\033[0m")
        except Exception:
            pass

    # 5. Launch Browser with Cache-Busting Version Query
    v = int(time.time())
    studio_url = f"http://localhost:8000/?v={v}"

    print("\n\033[92m" + "-" * 78)
    print("  [+] CONTRACTMIND v1.5 IS ONLINE & READY!")
    print(f"  - Studio Interface:    {studio_url} (Alpine.js Framework)")
    print("  - Port 3000 Redirect:  http://localhost:3000 -> http://localhost:8000")
    print("  - Backend API:         http://localhost:8000/api/v1")
    print("  - Swagger API Docs:    http://localhost:8000/docs")
    print("  - MCP FastServer:      http://localhost:8000/mcp/tools")
    print("-" * 78 + "\033[0m")

    try:
        webbrowser.open(studio_url)
    except Exception:
        pass

    print("\n\033[96m[*] System is running in this single console. Press CTRL+C at any time to stop.\033[0m")

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
