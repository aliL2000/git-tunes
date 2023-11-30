from authorization.spotify_auth import get_authorization_URL, get_refresh_token, get_authorization_code, get_new_token
import threading
from selenium import webdriver
import time

token = None
spotify_redirect_url = None

def check_for_url_change(driver, current_url):
    global spotify_redirect_url
    while True:
        new_url = driver.current_url
        if "https://localhost/?code" in new_url:
            spotify_redirect_url = new_url
            driver.quit()
            break  # Exit the loop when the URL changes
        time.sleep(1)  # Adjust the delay as needed

def obtain_spotify_authentication():
    token = get_refresh_token()
    if token:
        return token
    global spotify_redirect_url
    
    url_to_monitor = get_authorization_URL()
    # Set up the WebDriver (in this example, using Chrome)
    driver = webdriver.Chrome()
    driver.get(url_to_monitor)
    # Get the initial URL
    initial_url = driver.current_url

    # Start monitoring for URL changes in a separate thread
    monitor_thread = threading.Thread(target=check_for_url_change, args=(driver, initial_url))
    monitor_thread.start()
    time.sleep(1)
    monitor_thread.join()
    driver.quit()



    return get_new_token(get_authorization_code(spotify_redirect_url))