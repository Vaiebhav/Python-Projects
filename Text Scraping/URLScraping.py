import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Load the Excel file
excel_file = "input.xlsx"
df = pd.read_excel(excel_file)

# Create a directory to store extracted articles
output_directory = "extracted_articles"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to extract article text from a URL
def extract_article_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        
        # Find and extract the article title and text
        article_title = soup.find("title").get_text()
        article_paragraphs = soup.find_all("p")
        article_text = "\n".join([p.get_text() for p in article_paragraphs])
        
        return article_title, article_text
    else:
        return None, None
    
for index, row in df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]
    
    # Extract article title and text
    article_title, article_text = extract_article_text(url)
    
    if article_title and article_text:
        # Create a text file with the URL_ID as the file name
        output_file_path = os.path.join(output_directory, f"{url_id}.txt")
        
        # Write article title and text to the file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(article_title + "\n\n")
            output_file.write(article_text)
        
        print(f"Extracted and saved {output_file_path}")
    else:
        print(f"Failed to extract from URL_ID {url_id}")

print("Extraction and saving complete.")
