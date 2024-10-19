#Active and Passive Learning System

import requests
from bs4 import BeautifulSoup
import os
import json
import time
from threading import Timer

# Set threshold for schema strength
SCHEMA_THRESHOLD = 10  # Define the threshold below which passive learning will trigger

# Function to calculate schema strength
def calculate_schema_strength(schema_data):
    # Basic strength calculation based on the number of knowledge entries
    return len(schema_data)

# Function to fetch related information about a topic (Google search & scraping)
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

# Function to scrape content from Wikipedia pages
def scrape_wikipedia_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text_content = "\n".join([para.get_text() for para in paragraphs if para.get_text()])
    return text_content

# Function to store learned data and update schema
def store_learned_data(topic, data):
    file_name = f"{topic}_knowledge.json"
    
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            knowledge = json.load(file)
    else:
        knowledge = []
    
    knowledge.append(data)
    
    with open(file_name, "w") as file:
        json.dump(knowledge, file, indent=4)
    
    print(f"Knowledge about '{topic}' stored successfully.")

# Function to actively learn about a topic and store initial knowledge
def learn_about_topic(topic):
    print(f"Learning about '{topic}'...")
    links = fetch_information(topic)
    
    for link in links:
        print(f"Scraping content from: {link}")
        new_data = scrape_wikipedia_page(link)
        store_learned_data(topic, new_data)
        time.sleep(2)  # Adding sleep to simulate more natural fetching

# Function to check schema strength and learn passively if needed
def passive_learning(topic):
    file_name = f"{topic}_knowledge.json"
    
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            knowledge = json.load(file)
    else:
        knowledge = []
    
    # Step 1: Check schema strength
    schema_strength = calculate_schema_strength(knowledge)
    
    # Step 2: Trigger passive learning if strength is below threshold
    if schema_strength < SCHEMA_THRESHOLD:
        print(f"Schema for '{topic}' is weak (strength: {schema_strength}). Learning passively...")
        links = fetch_information(topic)
        
        for link in links:
            print(f"Scraping new content from: {link}")
            new_data = scrape_wikipedia_page(link)
            store_learned_data(topic, new_data)
            time.sleep(2)
        
        print(f"Passive learning for '{topic}' completed.")
    else:
        print(f"Schema for '{topic}' is strong (strength: {schema_strength}). No passive learning needed.")

# Function to assess all schemas periodically for passive learning
def assess_schemas(schemas):
    for topic in schemas:
        passive_learning(topic)

# Function to schedule periodic schema assessments (passive learning)
def start_passive_learning(schemas, interval=3600):
    # Assess schemas at the specified interval (in seconds)
    Timer(interval, lambda: assess_schemas(schemas)).start()

# Function to learn about a topic and start passive monitoring
def learn_and_monitor(topic):
    # Learn actively about a topic first
    learn_about_topic(topic)
    
    # Start passive learning and periodic assessments
    start_passive_learning([topic], interval=10)  # Check every 10 seconds for demo purposes

# Function to answer questions about a topic based on learned knowledge
def answer_question(topic, question):
    file_name = f"{topic}_knowledge.json"
    
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            knowledge = json.load(file)
    else:
        return f"Sorry, I don't know much about '{topic}' yet."
    
    # Search knowledge for an answer
    answer = None
    for fact in knowledge:
        if question.lower() in fact.lower():
            answer = fact
            break
    
    if answer:
        return f"Answer to your question: {answer}"
    else:
        return f"I couldn't find an exact answer in my current knowledge about '{topic}'."

# Entry point for the program
if __name__ == "__main__":
    # Step 1: Learn about a topic
    topic_of_interest = input("Enter a topic of interest: ")
    learn_and_monitor(topic_of_interest)
    
    # Step 2: Answer questions
    while True:
        user_question = input(f"Ask a question about '{topic_of_interest}' or type 'exit': ")
        if user_question.lower() == 'exit':
            break
        print(answer_question(topic_of_interest, user_question))
