import requests
import pandas as pd

url = "https://api.mfapi.in/mf/125497"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    print("Scheme Name:", data["meta"]["scheme_name"])

    nav_df = pd.DataFrame(data["data"])

    nav_df.to_csv(
        "Data/raw/live_nav_hdfc_top100.csv",
        index=False
    )

    print("NAV data saved successfully!")
    print("Rows:", len(nav_df))

else:
    print("API Error:", response.status_code)