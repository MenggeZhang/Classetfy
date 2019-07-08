import constants
import requests
import string
import re
import csv
import collections
import urllib.request
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

def html_tag_freq(html_text, tags=constants.HTML_TAGS):
    """
    return a list of tuples (html_tag, freq_count) in the html_text (string).
    """
    ret = []
    for tag in tags:
        ret.append((tag, html_text.count('<{}'.format(tag))))
    return ret

def html_word_freq(html_text, filter_common_stop_words=True, filter_invisible_text=True):
    """
    return a list of tuples (word, freq_count) in the html_text (string).
    Note the words are all converted to lowercase and leading/trailing spaces removed,
    words can only start with [a-z].
    If filter_common_stop_words is set to True, common English stop words are removed.
    If filter_invisible_text is set to True, only the visible text of the webpage is counted.
    """
    soup = BeautifulSoup(html_text, "lxml")
    text_context = soup.findAll(text=True)
    def all_alphabet_word(element):
        for c in element:
            if c not in string.ascii_lowercase:
                return False
        return True
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True
    if filter_invisible_text:
        text_context = filter(visible, text_context)
    sentences = [x.strip().lower() for x in text_context if x.strip()]
    words_list = []
    counter = collections.defaultdict(int)
    if filter_common_stop_words:
        english_stopwords = set(stopwords.words('english'))
        for sentence in sentences:
            for word in filter(lambda w: all_alphabet_word(w) and w not in english_stopwords, sentence.split()):
                counter[word] += 1
    else:
        for sentence in sentences:
            for word in filter(lambda w: all_alphabet_word(w), sentence.split()):
                counter[word] += 1
    return counter.items()

def write_freq_counts_to_csv(freq_count_list, output_fname):
    with open(output_fname, 'w') as f:
        for name, freq in freq_count_list:
            f.write('{},{}\n'.format(name, freq))

full_html_list = []
list_freader = csv.reader(open('/Users/menggezhang/Documents/Insights_CyCognito/full_html_list.txt'))
for row in list_freader:
    full_html_list.append(row[0])

for html_name in full_html_list:

    with open('/Users/menggezhang/Documents/Insights_CyCognito/HTML_Text_Files/'+html_name, 'r') as file:
        data = file.read().replace('\n', '')
        write_freq_counts_to_csv(html_tag_freq(data), '/Users/menggezhang/Documents/Insights_CyCognito/tag_feature_vecs/'+html_name+'.csv')
        write_freq_counts_to_csv(html_word_freq(data), '/Users/menggezhang/Documents/Insights_CyCognito/text_feature_vecs/'+html_name+'.csv')
