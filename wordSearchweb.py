import requests
from bs4 import BeautifulSoup

def find_word(url, word):
    """
    Fetches the HTML content of a web page or an entire website and searches for a specific word or phrase.

    Args:
        url (str): The URL of the web page or website.
        word (str): The word or phrase to search for.

    Returns:
        str: A markdown-formatted string indicating whether the word was found or not.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        content = response.text
        soup = BeautifulSoup(response.content, "html.parser")

        if word in content:
            return f"The word '{word}' was found on {url}."
        else:
            return f"The word '{word}' was not found on {url}."

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the content: {e}"

# Example usage
url = "https://syllabus.s.isct.ac.jp/courses/2025/7/0-907-0-110100-0/202538271"
word = "科目コード"
result = find_word(url, word)
print(result)
