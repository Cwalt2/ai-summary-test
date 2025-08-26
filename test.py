#
# A simple Command Line Interface (CLI) tool for local file summarization.
# This script takes a file path as an argument and prints a summary to the console.
#
# To run this script:
# 1. Ensure you have Python and pip installed.
# 2. Install the necessary libraries:
#    pip install spacy
# 3. Download a spaCy model:
#    python -m spacy download en_core_web_sm
# 4. Save this script as a Python file (e.g., summarize.py).
# 5. Run the script from your terminal, providing the file path as an argument:
#    python summarize.py path/to/your/file.txt
#
# Note: This is a basic example and is not production-ready.
# The summarization algorithm is simple and the script only works with .txt files.
#

import argparse
import spacy
from collections import Counter
from string import punctuation
import os

# --- 1. Load the spaCy model once ---
# We use a smaller model here to keep the CLI tool lightweight and fast.
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print("SpaCy model 'en_core_web_trf' not found. Please run:")
    print("python -m spacy download en_core_web_sm")
    exit()

# --- 2. Define the summarization logic function ---
def summarize_text(text, percentage=0.3):
    """
    Summarizes a given text using spaCy and a basic text-ranking algorithm.
    """
    if not text:
        return "No text to summarize."
    
    # Process the text with the loaded spaCy model
    doc = nlp(text)

    # Calculate word frequency
    word_frequencies = Counter()
    for word in doc:
        if word.text.lower() not in punctuation:
            word_frequencies[word.text.lower()] += 1

    # Normalize the frequencies
    max_frequency = max(word_frequencies.values()) if word_frequencies else 1
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    # Score sentences based on word frequencies
    sentence_scores = Counter()
    for sentence in doc.sents:
        for word in sentence:
            if word.text.lower() in word_frequencies.keys():
                sentence_scores[sentence] += word_frequencies[word.text.lower()]

    # Sort sentences by score to get the most important ones
    sorted_sentences = sorted(sentence_scores.keys(), key=lambda s: sentence_scores[s], reverse=True)

    # Select the top sentences to form the summary
    num_sentences_to_include = int(len(list(doc.sents)) * percentage)
    summary_sentences = sorted_sentences[:num_sentences_to_include]

    # Join the selected sentences and return the summary
    final_summary = ' '.join([s.text for s in summary_sentences])
    return final_summary or "Could not generate a summary. The text might be too short."

# --- 3. Set up the command-line argument parser ---
def main():
    parser = argparse.ArgumentParser(description="Summarize a text file using a simple AI algorithm.")
    parser.add_argument("file_path", type=str, help="The path to the .txt file to summarize.")

    args = parser.parse_args()
    file_path = args.file_path

    # --- 4. Validate and process the file ---
    if not os.path.exists(file_path):
        print(f"Error: The file at '{file_path}' does not exist.")
        return

    if not file_path.lower().endswith('.txt'):
        print("Error: This tool only supports .txt files.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Summarize the file content
        summary = summarize_text(text)
        
        # Print the results
        print("\n--- Original File Summary ---")
        print(summary)
        print("---------------------------\n")

    except Exception as e:
        print(f"An error occurred while reading or summarizing the file: {e}")

if __name__ == "__main__":
    main()
