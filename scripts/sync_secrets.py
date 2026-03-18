import base64, os, requests, sys
from nacl import encoding, public

def encrypt(pub_key: str, value: str) -> str:
    key = public.PublicKey(pub_key.encode(), encoding.Base64Encoder())
    return base64.b64encode(public.SealedBox(key).encrypt(value.encode())).decode()

repo = sys.argv[1]
hdr = {"Authorization": f"token {os.environ['REPO_PAT']}", "Accept": "application/vnd.github+json"}
pk = requests.get(f"https://api.github.com/repos/{repo}/actions/secrets/public-key", headers=hdr).json()

secrets = {}
for line in open(".env"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        secrets[k.strip()] = v.strip()

for k, v in secrets.items():
    requests.put(f"https://api.github.com/repos/{repo}/actions/secrets/{k}",
                 headers=hdr, json={"encrypted_value": encrypt(pk["key"], v), "key_id": pk["key_id"]})

print(f"Synced {len(secrets)} secrets to {repo}")
