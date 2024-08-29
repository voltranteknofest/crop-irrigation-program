import subprocess
import os
from dotenv import load_dotenv


load_dotenv()


def save_to_dashboard(moisture, area):
    match (area):
        case 0:
            api_url = os.getenv("API_URL_A")
        case 1:
            api_url = os.getenv("API_URL_B")
        case 2:
            api_url = os.getenv("API_URL_C")
        case 3:
            api_url = os.getenv("API_URL_D")
        case _:
            print("ERROR: Something is wrong with saving to dashboard.")
            return

    curl = [
        "curl", "-v", "-X", "POST", api_url,
        "--header", "Content-Type:application/json",
        "--data", f'{{"moisture": {moisture}}}'
    ]

    subprocess.run(curl, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


for i in range(4):
    save_to_dashboard(0, i)
