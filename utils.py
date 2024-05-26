import requests
import os
from dotenv import load_dotenv
import threading
import time

load_dotenv()

LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
PRE_PROMPT = os.getenv("PRE_PROMPT")

# Mutex for thread synchronization
mutex = threading.Lock()

# Time interval for debounce in milliseconds
DEBOUNCE_INTERVAL = 1000

# Last call time initialization
last_call_time = 0

def debounced_llama_call(prompt):
    global last_call_time
    
    # Acquire the mutex for thread safety
    mutex.acquire()

    # Get the current time
    current_time = time.time()

    # Calculate the time difference between current and last call
    time_diff = current_time - last_call_time

    # If the time difference is less than debounce interval, sleep for remaining time
    if time_diff < DEBOUNCE_INTERVAL / 1000:
        time.sleep((DEBOUNCE_INTERVAL / 1000) - time_diff)

    # Update the last call time
    last_call_time = time.time()

    # Release the mutex
    mutex.release()

    # Make the API request
    payload = {
        "prompt": PRE_PROMPT + "\n" + prompt,
        "temperature": 0.7,  # Adjust temperature as desired
        "max_tokens": 150  # Adjust max tokens as desired
    }
    headers = {"Authorization": f"Bearer {LLAMA_API_KEY}"}
    response = requests.post("https://api.llama.ai/v1/generate", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["text"]

# Example usage
print(debounced_llama_call("Your prompt here"))
