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
        self.__username = username
        self.__password = password
        self.__driver = None
        self.__cookies = None
        self.__visible_chatbox_driver = None

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_driver(self):
        return self.__driver

    def set_driver(self, driver):
        self.__driver = driver

    def get_cookies(self):
        return self.__cookies

    def set_cookies(self, cookies):
        self.__cookies = cookies

    def get_visible_chatbox_driver(self):
        return self.__visible_chatbox_driver

    def set_visible_chatbox_driver(self, driver):
        self.__visible_chatbox_driver = driver

    def create_headless_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.__driver = webdriver.Chrome(options=chrome_options)

    def login_with_cookies(self, cookies):
        if not self.__driver:
            self.create_headless_driver()
        self.__driver.get("https://www.linkedin.com")
        for cookie in cookies:
            self.__driver.add_cookie(cookie)
        self.__driver.refresh()

        try:
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            self.__cookies = cookies
            return True
        except TimeoutException:
            return False

    def login_to_linkedin(self):
        if not self.__driver:
            self.create_headless_driver()

        self.__driver.get("https://www.linkedin.com/login")
        try:
            username_field = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(self.__username)

            password_field = self.__driver.find_element(By.ID, "password")
            password_field.send_keys(self.__password)

            submit_button = self.__driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()

            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            self.__cookies = self.__driver.get_cookies()
            return True
        except TimeoutException:
            print("Login failed or took too long.")
            return False

    def login_to_linkedin_visible_then_headless(self):
        visible_driver = create_visible_driver()
        if login_to_linkedin(self.__username, self.__password, visible_driver):
            self.__cookies = visible_driver.get_cookies()
            visible_driver.quit()

            self.__driver = create_headless_driver()
            self.__driver.get("https://www.linkedin.com")
            for cookie in self.__cookies:
                self.__driver.add_cookie(cookie)
            self.__driver.refresh()
            return True
        else:
            visible_driver.quit()
            return False

    def login_to_linkedin_headless(self):
        self.__driver = create_visible_driver()  #using visible rn for test, headless vers: self.__driver = create_headless_driver()
        return login_to_linkedin(self.__username, self.__password, self.__driver)

    def check_for_new_messages(self, clients):
        if not self.__driver:
            print("No active driver. Please log in first.")
            return []

        clients_with_new_messages = []

        try:
            self.__driver.get("https://www.linkedin.com/messaging/?filter=unread")

            WebDriverWait(self.__driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-conversation-listitem__link"))
            )

            conversation_items = self.__driver.find_elements(By.CSS_SELECTOR, ".msg-conversation-listitem__link")

            for client in clients:
                linkedin_name = client.get_linkedin_name()
                if not linkedin_name:
                    print(f"Skipping client {client.get_name()} - No LinkedIn name provided.")
                    continue

                for item in conversation_items:
                    try:
                        name_element = item.find_element(By.CSS_SELECTOR, ".msg-conversation-listitem__participant-names")

                        if linkedin_name.lower() in name_element.text.lower():
                            clients_with_new_messages.append(client)
                            print(f"New message detected from {linkedin_name}")
                            client.set_has_responded(True)
                            break
                    except NoSuchElementException:
                        continue

            return clients_with_new_messages

        except TimeoutException:
            print("No messages found")
        except Exception as e:
            print(f"An error occurred while checking for new messages: {str(e)}")

        return clients_with_new_messages

    def open_linkedin_conversation(self, profile_url):
        full_name = self.get_linkedin_profile_name(profile_url)
        if not full_name:
            print(f"Failed to get profile name from URL: {profile_url}")
            return False

        try:
            print("Attempting to navigate to messaging...")
            messaging_link = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "li.global-nav__primary-item:nth-child(4) > a:nth-child(1)"))
            )
            print(f"Messaging link found. href: {messaging_link.get_attribute('href')}")
            messaging_link.click()
            time.sleep(1)
            print("Successfully clicked on messaging link")

            print("Waiting for search input...")
            search_input = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search messages']"))
            )
            print("Search input found")

            print(f"Searching for {full_name}...")
            search_input.send_keys(full_name)
            search_input.send_keys(Keys.RETURN)
            print("Search query sent")

            print("Waiting for search results...")
            first_result = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-conversation-listitem__link"))
            )
            print("First result found")

            print("Attempting to click on the first result...")
            first_result.click()
            print(f"Clicked on conversation with {full_name}")

            return True
        except TimeoutException as e:
            print(f"TimeoutException: {str(e)}")
            print(f"Failed to find element. Current URL: {self.__driver.current_url}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException: {str(e)}")
            print(f"Failed to find element. Current URL: {self.__driver.current_url}")
            return False
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Current URL: {self.__driver.current_url}")
            return False

    def open_linkedin_conversation_visible(self, client):
        if not self.__cookies:
            print("No cookies available. Please log in first.")
            return False

        full_name = client.get_linkedin_name()
        if not full_name:
            print(f"Client does not have a linkedin profile attached.")
            return False

        self.__visible_chatbox_driver = create_visible_driver()

        try:
            self.__visible_chatbox_driver.get("https://www.linkedin.com")
            for cookie in self.__cookies:
                self.__visible_chatbox_driver.add_cookie(cookie)
            self.__visible_chatbox_driver.refresh()

            WebDriverWait(self.__visible_chatbox_driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )

            self.__visible_chatbox_driver.get("https://www.linkedin.com/messaging/")

            print("Waiting for search input...")
            search_input = WebDriverWait(self.__visible_chatbox_driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search messages']"))
            )
            print("Search input found")

            print(f"Searching for {full_name}...")
            search_input.send_keys(full_name)
            search_input.send_keys(Keys.RETURN)
            print("Search query sent")

            print("Waiting for search results...")
            first_result = WebDriverWait(self.__visible_chatbox_driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-conversation-listitem__link"))
            )
            print("First result found")

            print("Attempting to click on the first result...")
            first_result.click()
            print(f"Clicked on conversation with {full_name}")

            return self.__visible_chatbox_driver
        except TimeoutException as e:
            print(f"TimeoutException: {str(e)}")
            print(f"Failed to find element. Current URL: {self.__visible_chatbox_driver.current_url}")
        except NoSuchElementException as e:
            print(f"NoSuchElementException: {str(e)}")
            print(f"Failed to find element. Current URL: {self.__visible_chatbox_driver.current_url}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print(f"Current URL: {self.__visible_chatbox_driver.current_url}")

        return False

    def get_conversation_text(self, profile_url):
        print(self.__driver)
        if not self.open_linkedin_conversation(profile_url):
            print(f"Failed to open conversation for profile: {profile_url}")
            return None

        try:
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-s-message-list.full-width.scrollable"))
            )

            message_list = self.__driver.find_element(By.CSS_SELECTOR, ".msg-s-message-list.full-width.scrollable")

            last_height = self.__driver.execute_script("return arguments[0].scrollHeight", message_list)
            while True:
                self.__driver.execute_script("arguments[0].scrollTop = -10000", message_list)
                time.sleep(0.5)

                new_height = self.__driver.execute_script("return arguments[0].scrollTop", message_list)
                print(f"Current height: {new_height}, Last height: {last_height}")
                if new_height == last_height:
                    break
                last_height = new_height

            messages = self.__driver.find_elements(By.CSS_SELECTOR, ".msg-s-message-list__event")
            print(f"Found {len(messages)} messages")

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
            message_input = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
            )
            message_input.click()
            print("Message input field found")

            print(f"Typing message: {message}")
            message_input.send_keys(message)
            time.sleep(0.5)
            try:
                message_send_button = WebDriverWait(self.__driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-form__send-btn"))
                )
            except TimeoutException:
                message_send_button = WebDriverWait(self.__driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-form__send-button"))
                )
            message_send_button.click()
            time.sleep(0.5)
            print("Message sent")

            return True
        except TimeoutException as e:
            print(f"TimeoutException: {str(e)}")
            print(f"Failed to send message. Current URL: {self.__driver.current_url}")
            return False
        except NoSuchElementException as e:
            print(f"NoSuchElementException: {str(e)}")
            print(f"Failed to send message. Current URL: {self.__driver.current_url}")
            return False
        except Exception as e:
            print(f"Unexpected error while sending message: {str(e)}")
            print(f"Current URL: {self.__driver.current_url}")
            return False

    def get_linkedin_profile_name(self, profile_url):
        linkedin_profile_pattern = r'^https?:\/\/(?:www\.)?linkedin\.com\/in\/[\w\-]+\/?$'
        if not re.match(linkedin_profile_pattern, profile_url):
            print("Invalid LinkedIn profile URL")
            return None

        try:
            self.__driver.get(profile_url)

            name_element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge"))
            )

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

    def quit(self):
        if self.__driver:
            self.__driver.quit()