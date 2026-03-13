import requests
import base64
import os
import json

filename = "safety_detector.py"
repo = "pdi999inc-lang/vibelenz-mvp"
token = "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"
branch = "main"

filepath = os.path.join(os.path.expanduser("~"), "Documents", filename)

print("Local path:", filepath)
print("File exists:", os.path.exists(filepath))

if not os.path.exists(filepath):
    raise SystemExit("Local file not found")

with open(filepath, "rb") as f:
    content = base64.b64encode(f.read()).decode("utf-8")

url = f"https://api.github.com/repos/{repo}/contents/{filename}"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json",
}

print("Checking repo/file on GitHub...")
get_resp = requests.get(url, headers=headers, params={"ref": branch})
print("GET status:", get_resp.status_code)
print(get_resp.text[:500])

sha = None
if get_resp.status_code == 200:
    sha = get_resp.json().get("sha")
elif get_resp.status_code != 404:
    raise SystemExit("GET request failed")

payload = {
    "message": "deploy safety_detector.py v2",
    "content": content,
    "branch": branch,
}

if sha:
    payload["sha"] = sha

print("Uploading...")
put_resp = requests.put(url, headers=headers, data=json.dumps(payload))
print("PUT status:", put_resp.status_code)
print(put_resp.text[:1000])
