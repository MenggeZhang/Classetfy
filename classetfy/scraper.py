import requests
import re
import collections
import urllib.request
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

from classetfy import constants

class Scraper:
    def __init__(self, url):
        if url.startswith('https://') or url.startswith('http://'):
            self.url = url
        else:
            self.url = 'http://' + url
        reqeust_data = requests.get(self.url)
        self.htmltext = reqeust_data.text
        self.soup = BeautifulSoup(self.htmltext, "lxml")
    
    def tag_frequencies(self, top_items=None):
        """
        return dictionary of number of times each html tag appears in a self.url
        """
        def count_html_tags_freqs(soup, tags):
            freq_count = {}
            for tag in constants.HTML_TAGS:
                freq = len(soup.find_all(tag))
                full_tag = '{}'.format(tag)
                freq_count[full_tag] = freq
            return freq_count
        freq_count = count_html_tags_freqs(self.soup, constants.HTML_TAGS)
        freq_entries = freq_count.items()
        freq_entries_sorted = sorted(freq_entries, key=lambda x: x[1], reverse=True)
        if top_items:
            return dict(freq_entries_sorted[:top_items])
        else:
            return dict(freq_entries_sorted)

    def tag_inner_text_frequencies(self):
        """
        return dictionary of number of times each html tag visible text (not necessarily single words)
        that appears in a self.url.
        all text converted to lowercase and leading/trailing spaces removed before counting.
        """
        text_context = self.soup.findAll(text=True)
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True
        result_visible = filter(visible, text_context)
        result_visible_lower = [x.strip().lower() for x in result_visible if x.strip()]
        result_visible_lower_alphanumeric = [re.sub(r'[^\w\s]','',x) for x in result_visible_lower]
        counter = collections.Counter(result_visible_lower_alphanumeric)
        return collections.OrderedDict(counter.most_common())

    def tag_inner_text_words_frequencies(self):
        """
        return dictionary of number of times each html tag visible text that is split into single words
        that appears in a self.url.
        all words converted to lowercase and leading/trailing spaces removed before counting.
        """
        symbols = ('.', ',', '@', '|', '-', '>')
        TOP_ITEMS = 25
        text_context = self.soup.findAll(text=True)
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True
        result = filter(visible, text_context)
        result_visible_lower = [x.strip().lower() for x in result if x.strip()] #sentence
        result_visible_lower_alpha = [re.sub(r'[^\w\s]','',x) for x in result_visible_lower]
        english_stopwords = set(stopwords.words('english'))
        words_list = []
        counter = collections.defaultdict(int)
        for sentence in result_visible_lower_alpha:
            split_words = list(filter(lambda w: not w in english_stopwords and not w in symbols and not w[0].isdigit(), sentence.split()))
            for word in split_words:
                counter[word] += 1
        word_freqs_sorted = sorted(counter.items(), key=lambda x : -x[1])
        return dict(word_freqs_sorted[:TOP_ITEMS])

