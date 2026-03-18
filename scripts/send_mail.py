import argparse, os, requests

API = "https://api.agentmail.to/v0"
HDR = {"Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}", "Content-Type": "application/json"}


def send(to: str, subject: str, body: str) -> dict:
    r = requests.post(f"{API}/inboxes/{os.environ['AGENTMAIL_INBOX_ID']}/messages/send",
                      headers=HDR, json={"to": to, "subject": subject, "text": body})
    r.raise_for_status()
    print(f"Sent: {r.json()['message_id']}")
    return r.json()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("to"); p.add_argument("subject"); p.add_argument("body")
    a = p.parse_args()
    send(a.to, a.subject, a.body)
