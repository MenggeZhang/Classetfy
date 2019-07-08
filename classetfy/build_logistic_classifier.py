import os.path
import sys
import csv
import os
import requests
import pandas
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle

import re
import collections
import urllib.request
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

from scraper import Scraper

########## predefined tags #########
HTML_TAGS = ('a', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 
'code', 'col', 'em', 'figure', 'footer', 'form', 'frame', 
'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'i', 'iframe', 
'img', 'input', 'label', 'li', 'link', 'main', 'map', 'meta', 
'noscript', 'option', 'p', 'param', 'picture', 'pie', 'ruby', 'script', 
'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'svg', 'table', 
'title', 'viedo')


def tag_frequencies(self):
    """
    return dictionary of number of times each html tag appears in a self.url
    """
    TOP_ITEMS = 25
    def count_html_tags_freqs(soup, tags):
        freq_count = []
        for tag in HTML_TAGS:
            freq = len(soup.find_all(tag))
            
        return freq_count
    freq_count = count_html_tags_freqs(self.soup, HTML_TAGS)
    return freq_count



def valid_ip(ip_addr):
    return True
    try:
        socket.inet_aton(ip_addr)
        return True
    except socket.error:
        return False

def ip_to_html_content(ip_addr):
    # given ip address, return the corresponding html content (string)
    
    res = requests.get('http://' + ip_addr, verify=False)
    res_text = res.text
        # return "<html>xxx</html>"
    return res_text

def main():
    internal_fname = "/Users/menggezhang/Documents/Insights_CyCognito/Internal_SuccessToOpen"
    customer_fname = "/Users/menggezhang/Documents/Insights_CyCognito/Customer_SuccessToOpen"

    internal_ips = []
    customer_ips = []

    internal_freader = csv.reader(open(internal_fname))
    # Reserve 10 ids as testing data
    for i in range(10):
        next(internal_freader)
    for row in internal_freader:
        internal_ips.append('http://'+row[0])

    customer_freader = csv.reader(open(customer_fname))
    # Reserve 10 ids as testing data
    for i in range(10):
        next(customer_freader)
    for row in customer_freader:
        customer_ips.append('http://'+row[0])

    internal_tags_freq=[]
    customer_tags_freq=[]

    for ip_addr in internal_ips:
        try:
            scraper = Scraper(ip_addr)
            freq_count = scraper.tag_frequencies()
            internal_tags_freq.append(freq_count)

        except Exception as e:
            pass

    for ip_addr in customer_ips:
        try:
            scraper = Scraper(ip_addr)
            freq_count = scraper.tag_frequencies()
            internal_tags_freq.append(freq_count)
        except Exception as e:
            pass

    print(type(internal_tags_freq))

        
    

    

if __name__ == "__main__":
    
    main()