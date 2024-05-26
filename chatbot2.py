import os
import tkinter as tk  # Example UI library
import requests  # For making API calls
from utils import debounced_llama_call  # Your debounced function
import streamlit as st

# Load the API key from the .env file
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
PRE_PROMPT = os.getenv("PRE_PROMPT")

chat_history = []

def create_chatbot_window():
    window = tk.Tk()
    window.title("Chatbot")
  # Input field for user prompts
    prompt_entry = tk.Entry(window, width=50)
    prompt_entry.pack(padx=10, pady=10)

  # Button to trigger response generation
    submit_button = tk.Button(window, text="Ask", command=lambda: get_llama_response(prompt_entry.get()))
    submit_button.pack(padx=10, pady=10)

  # Display area for chatbot responses and chat history
    chat_display = tk.Text(window, height=20, width=80)
    chat_display.pack()

  # Example dropdown menu using tkinter (modify for your UI framework)
    def update_selected_model(model_name):
        global selected_model  # Assuming a global variable for selected model
        selected_model = model_name
     # Update API endpoint or parameters based on the selected model
    models = ["Llama v1", "Llama v2"]  # Replace with available models
    selected_model = models[0]  # Initial selection

    model_dropdown = tk.OptionMenu(window, tk.StringVar(window, selected_model), *models, command=update_selected_model)
    model_dropdown.pack(padx=10, pady=10)

    window.mainloop()

def update_chat_display(prompt, response, chat_display):
    chat_history.append({"prompt": prompt, "response": response})
    chat_display_text = "\n".join([f"{entry['prompt']}: {entry['response']}" for entry in chat_history])
    chat_display.delete(1.0, tk.END)
    chat_display.insert(tk.END, chat_display_text)


def get_llama_response(prompt):
  # Replace with your actual debounced_llama_call function logic
    response = debounced_llama_call(prompt, PRE_PROMPT, LLAMA_API_KEY)
    update_chat_display(prompt, response)


create_chatbot_window()
