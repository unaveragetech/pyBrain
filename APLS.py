# Active and Passive Learning System
from pipin import install_requirements
install_requirements()

import requests
from bs4 import BeautifulSoup
import os
import json
import time
from threading import Timer
import logging

# Configure logging
logging.basicConfig(filename='learning_system.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
SCHEMA_THRESHOLD = 5  # Define the threshold below which passive learning will trigger

# Function to calculate schema strength
def calculate_schema_strength(schema_data):
    return len(schema_data.get("definitions", []))  # Calculate strength based on definitions count

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
        # Extract the actual URL if it starts with "/url?q="
        if href.startswith("/url?q="):
            # Decode the URL
            actual_url = href.split("/url?q=")[1].split("&")[0]  # Take the URL and discard additional parameters
            if "wikipedia.org/wiki/" in actual_url:
                links.append(actual_url)
                if len(links) >= 3:  # Limit to top 3 results for this example
                    break
    return links

# Function to scrape content from Wikipedia pages
def scrape_wikipedia_page(url):
    logging.info(f"Scraping Wikipedia page: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text_content = "\n".join([para.get_text() for para in paragraphs if para.get_text()])
    return text_content

# Function to store learned data and update schema
def store_learned_data(topic, data):
    file_name = f"{topic}_knowledge.json"

    # Initialize schema structure if the file does not exist
    if not os.path.exists(file_name):
        schema = {
            "topic": topic,
            "definitions": [],
            "examples": [],
            "use_cases": [],
            "related_topics": [],
            "sources": []
        }
    else:
        with open(file_name, "r") as file:
            schema = json.load(file)

    # Update the schema with new data
    if "definition" in data:
        schema["definitions"].append(data["definition"])
    if "example" in data:
        schema["examples"].append(data["example"])
    if "use_case" in data:
        schema["use_cases"].append(data["use_case"])
    if "related_topic" in data:
        schema["related_topics"].append(data["related_topic"])
    if "source" in data:
        schema["sources"].append(data["source"])

    # Save updated schema
    with open(file_name, "w") as file:
        json.dump(schema, file, indent=4)

    logging.info(f"Knowledge about '{topic}' updated successfully with new data: {data}")

# Function to actively learn about a topic and store initial knowledge
def learn_about_topic(topic):
    logging.info(f"Learning about '{topic}'...")
    links = fetch_information(topic)

    for link in links:
        new_data = scrape_wikipedia_page(link)
        data_to_store = {
            "definition": new_data.split('.')[0],  # Taking the first sentence as a definition
            "example": new_data.split('.')[1] if '.' in new_data else "",  # Second sentence as an example
            "use_case": "",  # You could enhance this with more specific scraping logic
            "related_topic": "",  # Placeholder for future improvements
            "source": link
        }
        store_learned_data(topic, data_to_store)
        time.sleep(2)  # Adding sleep to simulate more natural fetching

# Function to check schema strength and learn passively if needed
def passive_learning(topic):
    file_name = f"{topic}_knowledge.json"

    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            schema = json.load(file)
    else:
        logging.warning(f"No knowledge file found for '{topic}'. Initiating active learning.")
        learn_about_topic(topic)
        return

    # Step 1: Check schema strength
    schema_strength = calculate_schema_strength(schema)

    # Step 2: Trigger passive learning if strength is below threshold
    if schema_strength < SCHEMA_THRESHOLD:
        logging.info(f"Schema for '{topic}' is weak (strength: {schema_strength}). Learning passively...")
        links = fetch_information(topic)

        for link in links:
            new_data = scrape_wikipedia_page(link)
            data_to_store = {
                "definition": new_data.split('.')[0], 
                "example": new_data.split('.')[1] if '.' in new_data else "", 
                "use_case": "",
                "related_topic": "",
                "source": link
            }
            store_learned_data(topic, data_to_store)
            time.sleep(2)

        logging.info(f"Passive learning for '{topic}' completed.")
    else:
        logging.info(f"Schema for '{topic}' is strong (strength: {schema_strength}). No passive learning needed.")

# Function to assess all schemas periodically for passive learning
def assess_schemas(schemas):
    for topic in schemas:
        passive_learning(topic)

# Function to schedule periodic schema assessments (passive learning)
def start_passive_learning(schemas, interval=3600):
    Timer(interval, lambda: assess_schemas(schemas)).start()

# Function to learn about a topic and start passive monitoring
def learn_and_monitor(topic):
    learn_about_topic(topic)
    start_passive_learning([topic], interval=10)  # Check every 10 seconds for demo purposes

# Function to answer questions about a topic based on learned knowledge
def answer_question(topic, question):
    file_name = f"{topic}_knowledge.json"

    # Check if knowledge exists, if not, learn about the topic first
    if not os.path.exists(file_name):
        learn_about_topic(topic)

    with open(file_name, "r") as file:
        schema = json.load(file)

    # Search schema for an answer
    answer = None
    if "definitions" in schema:
        for definition in schema["definitions"]:
            if question.lower() in definition.lower():
                answer = definition
                break

    if answer:
        return f"Answer to your question: {answer}"
    else:
        return f"I couldn't find an exact answer in my current knowledge about '{topic}'. Learning new information..."

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
