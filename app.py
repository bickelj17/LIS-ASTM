"""
Flask web app for ASTM result file analysis.
Run: python app.py
- You: http://127.0.0.1:5000
- Teammates (same network): http://<your-IP>:5000  (printed when server starts)
No Gradio or shared links required.
"""
import html
import io
import socket
import sys
import tempfile
import threading
import webbrowser
from pathlib import Path

from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename

from line_checks import scrape_lines
from astm_checks import test_type, check_patient, check_qc, check_calibration

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4 MB max upload

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASTM Result File Analysis</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
        h1 { margin-bottom: 0.5rem; }
        p { color: #555; margin-bottom: 1.5rem; }
        form { margin-bottom: 1.5rem; }
        input[type="file"] { margin-bottom: 0.75rem; display: block; }
        button {
            background: #2563eb; color: white; border: none; padding: 0.5rem 1rem;
            border-radius: 6px; cursor: pointer; font-size: 1rem;
        }
        button:hover { background: #1d4ed8; }
        .output {
            background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
            padding: 1rem; white-space: pre-wrap; font-family: ui-monospace, monospace;
            font-size: 0.9rem; min-height: 80px;
        }
        .error {
            color: #b91c1c; font-weight: 600;
            background: #fef2f2; border: 1px solid #fecaca;
            border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1rem;
        }
        /* Lines inside analysis output that report failures */
        .output .error-line {
            color: #b91c1c; font-weight: 600;
            background: #fff1f2; display: inline; padding: 0.1em 0.25em;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>ASTM Result File Analysis</h1>
    <p>Upload an ASTM result file to run the LIS checks.</p>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".txt,.astm" required>
        <button type="submit">Analyze</button>
    </form>
    {% if result is not none %}
    <h2>File Analysis</h2>
    <div class="output">{{ result_html | safe }}</div>
    {% endif %}
    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
</body>
</html>
"""


def run_analysis(file_path: str) -> str:
    """Run the same checks as project(): read file, parse, run checks, return captured output."""
    with open(file_path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    parsed = scrape_lines(lines)
    t = test_type(parsed)

    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer
    try:
        if t == "P":
            check_patient(parsed, t)
        elif t == "Q":
            check_qc(parsed, t)
        elif t == "C":
            check_calibration(parsed, t)
        else:
            print("Unknown or invalid test type:", t)
    finally:
        sys.stdout = old_stdout
    return buffer.getvalue()


def result_to_html(text: str) -> str:
    """
    Turn captured stdout into HTML so lines that report problems stand out.
    Each line is escaped; error lines get a highlight span (Error: prefix, or
    'incorrect' / 'invalid' anywhere, matches line_checks output).
    """
    if not text:
        return ""
    chunks = []
    for line in text.splitlines():
        esc = html.escape(line)
        lower = line.lstrip().lower()
        is_error_line = (
            lower.startswith("error:")
            or "incorrect" in lower
            or "invalid" in lower
        )
        if is_error_line:
            chunks.append(f'<span class="error-line">{esc}</span>')
        else:
            chunks.append(esc)
    return "<br>\n".join(chunks)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    result_html = ""
    error = None
    if request.method == "POST":
        if "file" not in request.files:
            error = "No file selected."
            return render_template_string(
                INDEX_HTML, result=result, result_html=result_html, error=error
            )
        f = request.files["file"]
        if not f.filename:
            error = "No file selected."
            return render_template_string(
                INDEX_HTML, result=result, result_html=result_html, error=error
            )
        filename = secure_filename(f.filename)
        if not filename:
            filename = "upload.txt"
        try:
            # Each request gets its own private temp folder (auto-deleted on
            # exit) instead of a shared "uploads" folder next to the script.
            # That shared folder caused two people running this at the same
            # time (e.g. off a network share) to overwrite/delete each
            # other's in-progress upload.
            with tempfile.TemporaryDirectory(prefix="astm_upload_") as tmp_dir:
                path = Path(tmp_dir) / filename
                f.save(str(path))
                result = run_analysis(str(path))
                result_html = result_to_html(result)
        except Exception as e:
            error = str(e)
    return render_template_string(
        INDEX_HTML, result=result, result_html=result_html, error=error
    )


def _local_ip():
    """Get this machine's LAN IP so teammates can connect."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "?"


if __name__ == "__main__":
    port = 5000
    print("\n  ASTM Result Analysis")
    print("  --------------------")
    print(f"  Open in browser:   http://127.0.0.1:{port}")
    ip = _local_ip()
    if ip != "?":
        print(f"  For teammates:     http://{ip}:{port}")
        print("  (Teammates must be on the same network; allow Python in Windows Firewall if needed.)")
    print("  (Closing this window will stop the app.)\n")
    # Open browser after a short delay so the server is up
    def _open_browser():
        import time
        time.sleep(1.2)
        webbrowser.open(f"http://127.0.0.1:{port}")
    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=port, debug=False)
