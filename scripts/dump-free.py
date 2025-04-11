import requests
import json
import os

FETCH_FANTOME_API_TEMPLATE = "https://divineskinsapi.com/api/user/skins/fetch-fantome/{id}"
OUTPUT_DIR = "skins/free"

LOGIN_ENDPOINT = "https://divineskinsapi.com/auth/signin"
EMAIL = "<your_email>"
PASSWORD = "<your_password>"

FREE_SKINS_ENDPOINT = "https://divineskinsapi.com/api/user/skins/free"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get JWT token
JWT_TOKEN = None
response = requests.post(LOGIN_ENDPOINT, json={"email": EMAIL, "password": PASSWORD})
if response.status_code == 200:
    data = response.json()
    JWT_TOKEN = data["jwt"]
    print(f"Logged in as {data['username']}")
else:
    print(f"Failed to login: HTTP {response.status_code}")
    print(response.text)
    exit()

headers = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}

response = requests.get(FREE_SKINS_ENDPOINT, headers=headers)
skins = response.json()

for skin in skins:
    skin_id = skin["id"]
    name = skin["name"]
    artist = skin["artistUsername"]
    champion = skin["champion"]

    filename = f"{skin_id} - {name} by {artist} ({champion}).fantome"
    output_path = os.path.join(OUTPUT_DIR, filename)

    print(f"Downloading {filename}...")
    url = FETCH_FANTOME_API_TEMPLATE.format(id=skin_id)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(output_path, "wb") as out_file:
            out_file.write(response.content)
        print(f"Saved to {output_path}")
    else:
        print(f"Failed to download ID {skin_id}: HTTP {response.status_code}")

print("All downloads complete.")
