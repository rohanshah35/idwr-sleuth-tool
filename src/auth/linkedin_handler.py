import re
import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Creates and returns a visible Chrome WebDriver instance
def create_visible_driver():
    return webdriver.Chrome()


# Creates and returns a headless Chrome WebDriver instance
def create_headless_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)


# Logs into LinkedIn using the provided credentials and WebDriver
def login_to_linkedin(username, password, driver):
    driver.get("https://www.linkedin.com/login")
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys(username)

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-nav"))
        )
        return True
    except TimeoutException:
        print("Login failed or took too long.")
        return False


class LinkedInHandler:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.cookies = None
        self.visible_chatbox_driver = None

    def create_headless_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login_with_cookies(self, cookies):
        if not self.driver:
            self.create_headless_driver()
        self.driver.get("https://www.linkedin.com")
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            self.cookies = cookies
            return True
        except TimeoutException:
            return False

    def login_to_linkedin(self):
        if not self.driver:
            self.create_headless_driver()

        self.driver.get("https://www.linkedin.com/login")
        try:
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(self.username)

            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)

            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            self.cookies = self.driver.get_cookies()
            return True
        except TimeoutException:
            print("Login failed or took too long.")
            return False

    def get_cookies(self):
        return self.cookies

    # Logs into LinkedIn with a visible browser, then switches to headless mode
    def login_to_linkedin_visible_then_headless(self):
        visible_driver = create_visible_driver()
        if login_to_linkedin(self.username, self.password, visible_driver):
            self.cookies = visible_driver.get_cookies()
            visible_driver.quit()

            self.driver = create_headless_driver()
            self.driver.get("https://www.linkedin.com")
            for cookie in self.cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            return True
        else:
            visible_driver.quit()
            return False

    # Logs into LinkedIn using a headless browser
    def login_to_linkedin_headless(self):
        self.driver = create_visible_driver()  #using visible rn for test, headless vers: self.driver = create_headless_driver()
        return login_to_linkedin(self.username, self.password, self.driver)

    # Opens a conversation with a specified LinkedIn user
    def open_linkedin_conversation(self, profile_url):
        full_name = self.get_linkedin_profile_name(profile_url)
        if not full_name:
            print(f"Failed to get profile name from URL: {profile_url}")
            return False

        try:
            print("Attempting to navigate to messaging...")
            messaging_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "li.global-nav__primary-item:nth-child(4) > a:nth-child(1)"))
            )
            print(f"Messaging link found. href: {messaging_link.get_attribute('href')}")
            messaging_link.click()
            time.sleep(1)
            print("Successfully clicked on messaging link")

            print("Waiting for search input...")
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search messages']"))
            )
            print("Search input found")

            print(f"Searching for {full_name}...")
            search_input.send_keys(full_name)
            search_input.send_keys(Keys.RETURN)
            print("Search query sent")

            print("Waiting for search results...")
            first_result = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-conversation-listitem__link"))
            )
            print("First result found")

            print("Attempting to click on the first result...")
            first_result.click()
            print(f"Clicked on conversation with {full_name}")

            return True
        except TimeoutException as e:
            print(f"TimeoutException: {str(e)}")
            print(f"Failed to find element. Current URL: {self.driver.current_url}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException: {str(e)}")
            print(f"Failed to find element. Current URL: {self.driver.current_url}")
            return False
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            return False

    def open_linkedin_conversation_visible(self, profile_url):
        if not self.cookies:
            print("No cookies available. Please log in first.")
            return False

        full_name = self.get_linkedin_profile_name(profile_url)
        if not full_name:
            print(f"Failed to get profile name from URL: {profile_url}")
            return False

        self.visible_chatbox_driver = create_visible_driver()

        try:
            self.visible_chatbox_driver.get("https://www.linkedin.com")
            for cookie in self.cookies:
                self.visible_chatbox_driver.add_cookie(cookie)
            self.visible_chatbox_driver.refresh()

            WebDriverWait(self.visible_chatbox_driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )

            self.visible_chatbox_driver.get("https://www.linkedin.com/messaging/")

            print("Waiting for search input...")
            search_input = WebDriverWait(self.visible_chatbox_driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search messages']"))
            )
            print("Search input found")

            print(f"Searching for {full_name}...")
            search_input.send_keys(full_name)
            search_input.send_keys(Keys.RETURN)
            print("Search query sent")

            print("Waiting for search results...")
            first_result = WebDriverWait(self.visible_chatbox_driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-conversation-listitem__link"))
            )
            print("First result found")

            print("Attempting to click on the first result...")
            first_result.click()
            print(f"Clicked on conversation with {full_name}")

            return self.visible_chatbox_driver
        except TimeoutException as e:
            print(f"TimeoutException: {str(e)}")
            print(f"Failed to find element. Current URL: {self.visible_chatbox_driver.current_url}")
        except NoSuchElementException as e:
            print(f"NoSuchElementException: {str(e)}")
            print(f"Failed to find element. Current URL: {self.visible_chatbox_driver.current_url}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Current URL: {self.visible_chatbox_driver.current_url}")

        return False

    def get_conversation_text(self, profile_url):
        print(self.driver)
        if not self.open_linkedin_conversation(profile_url):
            print(f"Failed to open conversation for profile: {profile_url}")
            return None

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-s-message-list.full-width.scrollable"))
            )

            # Find the scrollable message list
            message_list = self.driver.find_element(By.CSS_SELECTOR, ".msg-s-message-list.full-width.scrollable")

            # Scroll to load older messages
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", message_list)
            while True:
                # Scroll to top
                self.driver.execute_script("arguments[0].scrollTop = -10000", message_list)
                time.sleep(0.5)  # Wait for content to load

                # Check if we've reached the top
                new_height = self.driver.execute_script("return arguments[0].scrollTop", message_list)
                print(f"Current height: {new_height}, Last height: {last_height}")  # Debug print
                if new_height == last_height:
                    break
                last_height = new_height

            # Now get all the messages
            messages = self.driver.find_elements(By.CSS_SELECTOR, ".msg-s-message-list__event")
            print(f"Found {len(messages)} messages")  # Debug print

            conversation_text = []
            for message in messages:
                try:
                    content = message.find_element(By.CSS_SELECTOR, ".msg-s-event-listitem__body").text
                    sender_element = message.find_element(By.CSS_SELECTOR, ".msg-s-message-group__name")
                    sender = sender_element.text if sender_element.is_displayed() else "You"
                    conversation_text.append(f"{sender}: {content}")
                except NoSuchElementException:
                    conversation_text.append(f"{content}")
            return conversation_text
        except TimeoutException:
            print("Failed to load conversation messages")
            return None

    def send_linkedin_message(self, profile_url, message):
        if not self.open_linkedin_conversation(profile_url):
            print(f"Failed to open conversation for profile: {profile_url}")
            return False

        try:
            print("Waiting for message input field...")
            message_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
            )
            message_input.click()
            print("Message input field found")

            print(f"Typing message: {message}")
            message_input.send_keys(message)
            time.sleep(0.5)
            try:
                message_send_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-form__send-btn"))
                )
            except TimeoutException:
                message_send_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-form__send-button"))
                )
            message_send_button.click()
            time.sleep(0.5)
            print("Message sent")

            return True
        except TimeoutException as e:
            print(f"TimeoutException: {str(e)}")
            print(f"Failed to send message. Current URL: {self.driver.current_url}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException: {str(e)}")
            print(f"Failed to send message. Current URL: {self.driver.current_url}")
            return False
        except Exception as e:
            print(f"Unexpected error while sending message: {str(e)}")
            print(f"Current URL: {self.driver.current_url}")
            return False

    def get_linkedin_profile_name(self, profile_url):
        # Verify the URL is a LinkedIn profile URL
        linkedin_profile_pattern = r'^https?:\/\/(?:www\.)?linkedin\.com\/in\/[\w\-]+\/?$'
        if not re.match(linkedin_profile_pattern, profile_url):
            print("Invalid LinkedIn profile URL")
            return None

        try:
            # Navigate to the profile page
            self.driver.get(profile_url)

            # Wait for the profile name to be visible
            name_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge"))
            )

            # Extract the full name
            full_name = name_element.text.strip()
            print(f"Profile name: {full_name}")
            return full_name

        except TimeoutException:
            print("Timeout while loading profile page or finding name element")
        except NoSuchElementException:
            print("Could not find the name element on the profile page")
        except Exception as e:
            print(f"An error occurred while retrieving the profile name: {str(e)}")

        return None

    # Quits the WebDriver, closing the browser
    def quit(self):
        if self.driver:
            self.driver.quit()

