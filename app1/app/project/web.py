from bs4 import BeautifulSoup
import requests
import mysql.connector

def scrape_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        s=soup.find('div',id='city')
        paragraphs = s.find_all('h3')
        content = '\n'.join([p.get_text() for p in paragraphs])
        connect_to_database(content)
        return content
    
    else:
        print("Failed to fetch the webpage.")
        return None

def connect_to_database(content):
    if content:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO questions (Question) VALUES (%s)"
        val = (content,)
        mycursor.execute(sql, val)

        mydb.commit()
        mydb.close()
    else:
        print("Content is empty. Skipping database insertion.")
    
    


if __name__ == "__main__":
    url = input("Enter the URL to scrape: ")
    scraped_content = scrape_content(url)
    if scraped_content:
        print("Scraped Content:")
        print(scraped_content)
    else:
        print("No content scraped.")
