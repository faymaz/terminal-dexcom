import os
import time
import requests
from pydexcom import Dexcom
from requests.exceptions import ConnectionError, Timeout

# Setup Dexcom authentication
dexcom = Dexcom(username="your_email_or_phone", password="your_password", ous=True)

# Path to the file where BG info will be written
bg_file = "/tmp/bg_info.txt"  # Using /tmp for temporary files on macOS

# Function to update the BG info file
def update_bg_info(glucose_value, trend_arrow):
    # Determine the color based on glucose levels
    if glucose_value >= 240:
        color_code = "\033[93m"  # Yellow
    elif glucose_value < 90:
        color_code = "\033[91m"  # Red
    elif 160 <= glucose_value < 240:
        color_code = "\033[93m"  # Yellow
    else:
        color_code = "\033[92m"  # Green

    # Format the BG info to be displayed in the prompt
    bg_info = f"{color_code}{glucose_value} mg/dL {trend_arrow}\033[0m"

    # Write the formatted BG info to the file
    with open(bg_file, 'w') as file:
        file.write(bg_info)

# Main function to check glucose levels and update the BG info file
def check_glucose():
    retries = 0
    max_retries = 5  # Maximum number of retries before giving up
    retry_delay = 10  # Delay in seconds before retrying

    while True:
        try:
            # Get the current blood glucose reading and trend
            glucose_reading = dexcom.get_current_glucose_reading()

            if glucose_reading is None:
                print("No glucose reading available at the moment.")
                time.sleep(60)  # Wait for 1 minute before retrying
                continue
            glucose_value = glucose_reading.value
            trend_arrow = glucose_reading.trend_arrow
            # Update the BG info file with the glucose value and trend arrow
            update_bg_info(glucose_value, trend_arrow)

            # Wait for 5 minutes (300 seconds)
            time.sleep(180) # 3 minutes

        except (ConnectionError, Timeout) as e:
            print(f"Error fetching glucose data: {e}")
            retries += 1
            if retries > max_retries:
                print("Max retries reached. Exiting.")
                break
            else:
                print(f"Retrying in {retry_delay} seconds... ({retries}/{max_retries})")
                time.sleep(retry_delay)
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            break  # Exit the loop if an unexpected error occurs

if __name__ == "__main__":
    check_glucose()
