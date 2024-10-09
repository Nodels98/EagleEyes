import requests
import time
from datetime import datetime

# Create a session to persist cookies
session = requests.Session()

# Login URL and payload
login_url = "https://my.goftino.com/a_signin"
payload = "email=PUT_GOFTINO_MANAGER_EMAIL_HERE&password=PUT_GOFTINO_MANAGER_PASSWORD_HERE"
login_headers = {

    # Remove the hardcoded cookie and use session persistence
    # Add as you wish
}
GOFTINO_ADMIN_ID = "some thing like this: 1372b2d34e36d277887d2299"
# Chat list URL
chat_list_url = f'https://my.goftino.com/action/chatlist/getlist/{GOFTINO_ADMIN_ID}'

# Initialize last processed message timestamp and message storage
last_processed_timestamp = None
unique_messages = {}

# List of blacklisted sender IDs (to be ignored)
blacklist_senders = [
    "operators_Goftino_IDs"  # Additional blacklisted sender IDs for filters operators messages from users
]

# Function to log in to Goftino
def login():
    response = session.post(login_url, headers=login_headers, data=payload)
    
    # Check if login was successful
    if response.status_code == 200 and "goftinoSession" in session.cookies:
        print("Login successful!")
    else:
        print("Login failed!")
        print(response.text)
        return False
    return True

# Function to extract messages
def extract_and_save():
    global last_processed_timestamp, unique_messages
    print("extracting...")
    # Fetch chat list
    response = session.get(chat_list_url)
    if response.status_code == 200:
        chat_data = response.json()
        
        # Extract messages and their text
        messages = chat_data.get("list", [])
        for message in messages:
            date = message.get("date", "")
            sender = message.get("sender", "")
            
            # Skip processing messages from blacklisted senders
            if sender in blacklist_senders:
                continue  # Ignore this message and move to the next one
            
            # Convert the date string to datetime for comparison
            date_obj = datetime.fromisoformat(date.replace("Z", "+00:00"))
            
            # Only process messages newer than the last processed one
            if last_processed_timestamp is None or date_obj > last_processed_timestamp:
                # Store the message with its date as the key to ensure uniqueness
                unique_messages[date] = message  # message is a dictionary
                
                # Update the last processed timestamp to avoid duplicates
                last_processed_timestamp = date_obj  # Update to the latest message timestamp
    else:
        print("Failed to fetch chat list")



# Function to save messages to a file
def save_messages():
    if unique_messages:
        # Get the current date and time for the filename
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Goftino_Monitoring/chat_log_{current_time}.txt"
        
        # Save the collected unique messages into the file
        with open(filename, "w", encoding="utf-8") as file:
            for msg in unique_messages.values():
                # Extract only the content of the 'text' key from each message
                text_content = msg.get('text', '')  # Use msg instead of message
                file.write(f"{text_content}\n")  # Write each message's text content followed by a newline

        print(f"Saved unique messages to {filename}")

# Main loop for collecting messages every 30 seconds for 15 minutes
if login():
    start_time = time.time()
    while True:
        extract_and_save()
        time.sleep(30)
        print(unique_messages)  # Sleep for 30 seconds
        print(time.time() - start_time)
        # Check if 15 minutes have passed
        if time.time() - start_time >= 900:  # 15 minutes (900 seconds)
            save_messages()
            unique_messages = {}
            start_time = time.time()
            # break  # Exit the loop after saving
else:
    print("Exiting the script due to failed login.")
