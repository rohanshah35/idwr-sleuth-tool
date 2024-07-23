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
        print("Successfully logged in!")
        return True
    except TimeoutException:
        print("Login failed or took too long.")
        return False


class LinkedInHandler:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None

    # Logs into LinkedIn with a visible browser, then switches to headless mode
    def login_to_linkedin_visible_then_headless(self):
        visible_driver = create_visible_driver()
        if login_to_linkedin(self.username, self.password, visible_driver):
            cookies = visible_driver.get_cookies()
            visible_driver.quit()

            self.driver = create_headless_driver()
            self.driver.get("https://www.linkedin.com")
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            return True
        else:
            visible_driver.quit()
            return False

    # Logs into LinkedIn using a headless browser
    def login_to_linkedin_headless(self):
        self.driver = create_visible_driver() #using visible rn for test, headless vers: self.driver = create_headless_driver()
        return login_to_linkedin(self.username, self.password, self.driver)

    # Opens a conversation with a specified LinkedIn user
    def open_linkedin_conversation(self, messenger_full_name):
        try:
            print("Attempting to navigate to messaging...")
            messaging_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "li.global-nav__primary-item:nth-child(4) > a:nth-child(1)"))
            )
            print(f"Messaging link found. href: {messaging_link.get_attribute('href')}")
            messaging_link.click()
            time.sleep(2)
            print("Successfully clicked on messaging link")

            print("Waiting for search input...")
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search messages']"))
            )
            print("Search input found")

            print(f"Searching for {messenger_full_name}...")
            search_input.send_keys(messenger_full_name)
            search_input.send_keys(Keys.RETURN)
            print("Search query sent")

            print("Waiting for search results...")
            first_result = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-conversation-listitem__link"))
            )
            print("First result found")

            print("Attempting to click on the first result...")
            first_result.click()
            print(f"Clicked on conversation with {messenger_full_name}")

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

    # Retrieves the text of a conversation with a specified LinkedIn user
    def get_conversation_text(self, messenger_full_name):
        self.open_linkedin_conversation(messenger_full_name)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-s-message-list__event"))
            )

            messages = self.driver.find_elements(By.CSS_SELECTOR, ".msg-s-message-list__event")

            conversation_text = []
            for message in messages:
                try:
                    sender = message.find_element(By.CSS_SELECTOR, ".msg-s-message-group__name").text
                    content = message.find_element(By.CSS_SELECTOR, ".msg-s-event-listitem__body").text
                    conversation_text.append(f"{sender}: {content}")
                except NoSuchElementException:
                    pass

            return "\n".join(conversation_text)
        except TimeoutException:
            print("Failed to load conversation messages")
            return None

    def send_linkedin_message(self, messenger_full_name, message):
        try:
            if not self.open_linkedin_conversation(messenger_full_name):
                print(f"Failed to open conversation with {messenger_full_name}")
                return False

            print("Waiting for message input field...")
            message_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
            )
            message_input.click()
            print("Message input field found")

            print(f"Typing message: {message}")
            message_input.send_keys(message)
            time.sleep(0.5)
            message_send_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-form__send-btn"))
            )
            message_send_button.click()
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

    # Quits the WebDriver, closing the browser
    def quit(self):
        if self.driver:
            self.driver.quit()


def main():
    # LinkedIn credentials
    linkedin_username = ""
    linkedin_password = ""

    # Recipient's full name as it appears on LinkedIn
    recipient_name = "Luca Bianchini"

    # Message to send
    message = "Hello! This is a test message sent using the LinkedInHandler."

    try:
        # Create LinkedInHandler instance
        linkedin_handler = LinkedInHandler(linkedin_username, linkedin_password)

        print("Logging in to LinkedIn...")
        if linkedin_handler.login_to_linkedin_headless():
            print("Login successful!")

            print(f"Attempting to send message to {recipient_name}...")
            if linkedin_handler.send_linkedin_message(recipient_name, message):
                print("Message sent successfully!")
            else:
                print("Failed to send message.")
        else:
            print("Failed to log in to LinkedIn.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if linkedin_handler:
            print("Closing browser...")
            linkedin_handler.quit()

if __name__ == "__main__":
    main()