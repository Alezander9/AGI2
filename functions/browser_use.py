import json, os, time, requests

API = "https://api.browser-use.com/api/v2"
HDR = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}


def browser_subagent(task: str, url: str | None = None) -> dict:
    body = {"task": task, "sessionSettings": {
        "profileId": os.environ.get("BROWSER_USE_PROFILE_ID"),
        "customProxy": {
            "host": os.environ["PROXY_HOST"],
            "port": int(os.environ["PROXY_PORT"]),
            "username": os.environ["PROXY_USER"],
            "password": os.environ["PROXY_PASS"],
        },
    }}
    if url:
        body["startUrl"] = url

    tid = requests.post(f"{API}/tasks", json=body, headers=HDR).json()["id"]
    print(f"Task {tid} started")

    while True:
        time.sleep(5)
        if requests.get(f"{API}/tasks/{tid}/status", headers=HDR).json()["status"] in ("finished", "stopped"):
            break

    detail = requests.get(f"{API}/tasks/{tid}", headers=HDR).json()
    os.makedirs("browser-use-traces", exist_ok=True)
    json.dump(detail, open(f"browser-use-traces/{tid}.json", "w"), indent=2)
    print(f"{detail['status']} | {detail.get('output', 'None')}")
    return detail
