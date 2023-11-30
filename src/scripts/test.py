
import threading
from authorization.spotify_auth import get_authorization_URL
from selenium import webdriver
import time

def check_for_url_change(driver, current_url):
    while True:
        new_url = driver.current_url
        print(f"Current URL: {new_url}")
            # Add your code here to handle th
        if new_url != current_url:
            print(f"URL changed: {new_url}")
            # Add your code here to handle the URL change as needed
            current_url = new_url  # Update the current_url for the next iteration
        time.sleep(5)  # Adjust the delay as needed

# Replace 'your_url' with the URL you want to monitor
url_to_monitor = get_authorization_URL()

# Set up the WebDriver (in this example, using Chrome)
driver = webdriver.Chrome()
driver.get(url_to_monitor)

# Get the initial URL
initial_url = driver.current_url

# Start monitoring for URL changes in a separate thread
monitor_thread = threading.Thread(target=check_for_url_change, args=(driver, initial_url))
monitor_thread.start()

# Other operations can be performed here while monitoring is ongoing

# Example: Keeping the main thread alive for some time
time.sleep(10)

# After a certain period, stop the monitoring thread and close the browser
monitor_thread.join()
driver.quit()