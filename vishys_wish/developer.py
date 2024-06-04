from constants import O_SETG
import requests
from bs4 import BeautifulSoup

username = O_SETG["developer"]["username"]
password = O_SETG["developer"]["password"]

# URLs
login_page_url = "https://developers.kite.trade/login"
dashboard_url = "https://developers.kite.trade/apps"

# Start a session
session = requests.Session()

# Step 1: Get the login page to retrieve CSRF token
response = session.get(dashboard_url, allow_redirects=True)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Find the CSRF token from the login page
csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
# Step 3: Prepare login data
login_data = {"username": username, "password": password, "csrf_token": csrf_token}

# Step 4: Submit the login form
login_response = session.post(login_page_url, data=login_data)

# Check if login was successful by looking at the response URL or content
if "incorrect" in login_response.text.lower():
    print("Login failed. Check your credentials.")
else:
    print("Login successful!")

    # Step 5: Navigate to the target page after login
    dashboard_response = session.get(dashboard_url)

    # Step 6: Parse the dashboard page to find the window.document.location
    dashboard_soup = BeautifulSoup(dashboard_response.text, "html.parser")
    print(dashboard_soup.prettify())
    # Find all the rows with the specific class and extract the URL from onclick
    apps = dashboard_soup.find_all("tr", class_="app")

    for app in apps:
        onclick_attr = app.get("onclick")
        if onclick_attr:
            # Extract the URL part from the onclick attribute
            location_url = onclick_attr.split("'")[1]
            full_url = f"https://developers.kite.trade{location_url}"
            print(f"Found URL: {full_url}")

            # Step 7: Make a request to the extracted URL
            app_response = session.get(full_url)

            # Step 8: Handle the response from the app page
            app_soup = BeautifulSoup(app_response.text, "html.parser")
            # Example: Print the app page content
            print(app_soup.prettify())

            # If you need to extract specific information from the app page, you can do it here
            # For example, extract some details
            # details = app_soup.find('div', class_='some-class').text
            # print(f"App Details: {details}")
