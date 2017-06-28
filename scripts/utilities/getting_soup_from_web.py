import requests

from bs4 import BeautifulSoup

def BSoup(url):
    '''INSERTING URL RETRIEVES DIRECTLY THE NEEDED SOUP FROM HTML WEBPAGE'''
    soup = BeautifulSoup(requests.get(url).text)
    return soup

