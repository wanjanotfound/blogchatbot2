import time
import requests
import nltk
from nltk import  word_tokenize
from nltk.corpus import wordnet
from rake_nltk import Rake


nltk.download('punkt')
nltk.download('wordnet')


# Debounce function to prevent rapid consecutive API calls
def debounce(func):
    last_called = 0
    
    def debounced(*args, **kwargs):
        nonlocal last_called
        
        now = time.time()
        if now - last_called < 0.5:  # Debounce interval: 0.5 seconds
            return "Please wait before asking another question."
        else:
            last_called = now
            return func(*args, **kwargs)
    
    return debounced

# Function for grammar correction
def correct_grammar(prompt):
       # Tokenize the prompt into words
    words = word_tokenize(prompt)

    # Correct each word using WordNet's built-in synonyms
    corrected_words = []
    for word in words:
        corrected_word = correct_word(word)
        corrected_words.append(corrected_word)

    # Join the corrected words back into a sentence
    corrected_sentence = ' '.join(corrected_words)

    return corrected_sentence

def correct_word(word):
    # Check if the word is in WordNet
    if wordnet.synsets(word):
        return word  # Word is correct
    else:
        # Try to find a similar word from WordNet
        synonyms = wordnet.synsets(word)
        if synonyms:
            return synonyms[0].lemmas()[0].name()  # Use the first synonym
        else:
            return word  # Unable to find a correction, return the original word

# Function for content suggestion
def suggest_content(prompt):
     # Extract keywords from the prompt
    r = Rake()
    r.extract_keywords_from_text(prompt)
    keywords = r.get_ranked_phrases()

    # Generate content based on the extracted keywords
    suggested_content = generate_content(keywords)

    return suggested_content

def generate_content(keywords):

    # Placeholder implementation for generating content
    query = ' '.join(keywords)

    # Make a request to a hypothetical content API
    response = requests.get(f"https://randomuser.me/api?query={query}")

    if response.status_code == 200:
        # Extract relevant content from the response
        content = response.json().get('content', "No content found")
    else:
        content = "Error: Unable to retrieve content"

    return content


    # You can use the extracted keywords to search for relevant content,
    
    
 
# Function to call the Llama API with debounce logic
@debounce
def debounced_llama_call(prompt,pre_prompt, api_key, selected_model):
    # Replace this with actual API call to Llama2 API
      # Construct the API endpoint URL
    endpoint = "https://llama2-api.example.com/endpoint"  # Replace with the actual API endpoint

    # Construct the request payload
    payload = {
        "prompt": prompt,
        "pre_prompt": pre_prompt,
        "api_key": api_key,
        "selected_model": selected_model
    }

    # Send POST request to the Llama2 API
    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code == 200:
            # Return the response text
            return response.text
        else:
            # Handle error responses
            return f"Error: {response.status_code}"
    except Exception as e:
        # Handle request exceptions
        return f"Error: {str(e)}"




    


