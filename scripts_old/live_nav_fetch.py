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
    import requests
import pandas as pd

schemes = [119551, 120503, 118632, 119092, 120841]

for code in schemes:
    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        nav_df.to_csv(
            f"Data/raw/nav_{code}.csv",
            index=False
        )

        print(f"Saved NAV for {code}")
        