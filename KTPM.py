#Knowledge Update through Passive Monitoring

import json
import os
import requests
from bs4 import BeautifulSoup
import difflib

SCHEMA_THRESHOLD = 10  # Threshold for triggering passive learning

# Function to calculate schema strength based on stored knowledge
def calculate_schema_strength(knowledge):
    return len(knowledge)

# Function to load existing knowledge for a topic from a file
def load_existing_knowledge(topic):
    file_name = f"{topic}_knowledge.json"
    
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            knowledge = json.load(file)
        return knowledge
    else:
        return []

# Enhanced function to fetch and validate information from reliable sources (e.g., Wikipedia)
def fetch_information(topic):
    search_url = f"https://www.google.com/search?q={topic}+site:wikipedia.org"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if "wikipedia.org/wiki/" in href:
            links.append(href)
            if len(links) >= 3:  # Limit to top 3 results for this example
                break
    return links

# Enhanced function to scrape and clean content from Wikipedia pages
def scrape_wikipedia_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    
    # Extract and clean text content
    text_content = "\n".join([para.get_text() for para in paragraphs if para.get_text()])
    return text_content

# Function to validate relevance of new information based on similarity to existing schema
def validate_information(new_data, knowledge):
    # Use difflib's SequenceMatcher to compare similarity between new data and existing schema knowledge
    for entry in knowledge:
        similarity = difflib.SequenceMatcher(None, new_data, entry).ratio()
        if similarity > 0.7:  # Consider data similar if similarity > 70%
            return False  # If similar information exists, discard new data
    return True  # Otherwise, the data is considered relevant and new

# Function to update schema only with validated and relevant information
def update_schema(topic, new_data):
    file_name = f"{topic}_knowledge.json"
    
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            knowledge = json.load(file)
    else:
        knowledge = []
    
    # Validate new data before updating schema
    if validate_information(new_data, knowledge):
        knowledge.append(new_data)
        
        # Save updated knowledge back to file
        with open(file_name, 'w') as file:
            json.dump(knowledge, file, indent=4)
        
        print(f"Schema for '{topic}' updated with new information.")
    else:
        print(f"New information for '{topic}' was found to be redundant or irrelevant.")

# Enhanced function to monitor and trigger passive learning with strict data validation
def monitor_and_learn_passively(topic):
    knowledge = load_existing_knowledge(topic)
    
    if calculate_schema_strength(knowledge) < SCHEMA_THRESHOLD:
        print(f"Schema for '{topic}' is weak. Triggering passive learning.")
        
        # Fetch new, relevant information
        links = fetch_information(topic)
        
        for link in links:
            print(f"Scraping content from: {link}")
            new_data = scrape_wikipedia_page(link)
            
            # Update schema with validated information
            update_schema(topic, new_data)
    
    else:
        print(f"Schema for '{topic}' is strong. No passive learning required.")

# Test monitoring for a known topic
if __name__ == "__main__":
    test_topic = "machine learning"
    monitor_and_learn_passively(test_topic)

