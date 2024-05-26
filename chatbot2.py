import os
import streamlit as st
from dotenv import load_dotenv
from utils import debounced_llama_call, correct_grammar, suggest_content

# Load the API key and other secrets from the .env file
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
PRE_PROMPT = "You are a helpful personal assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as a personal Assistant."

chat_history = []

def create_chatbot_window():
    st.title("Chatbot")
    
    # Input field for user prompts
    prompt = st.text_input("Ask something:", key="prompt")

    # Dropdown menu for selecting Llama model
    selected_model = st.selectbox("Select Llama Model", ["Llama v1", "Llama v2"], index=0)

    # Button to trigger response generation
    if st.button("Ask"):
        corrected_prompt = correct_grammar(prompt)
        response = debounced_llama_call(corrected_prompt, PRE_PROMPT, LLAMA_API_KEY, selected_model)
        st.text(response)
        
        # Suggest content based on prompt
        suggested_content = suggest_content(prompt)
        st.text(f"Suggested content: {suggested_content}")

    # Button for navigation to the blogging application
    if st.button("Go to Blogging App"):
        # Placeholder implementation for navigating to the blogging application
        # Replace this with actual implementation
        st.markdown("[Clikc here to Go to the blogging App](blogging App  url )")

    # Display area for chatbot responses and chat history
    st.subheader("Chat History")
    for entry in chat_history:
        st.text(f"{entry['prompt']}: {entry['response']}")

def update_chat_display(prompt, response):
    chat_history.append({"prompt": prompt, "response": response})

if __name__ == "__main__":
    create_chatbot_window()

