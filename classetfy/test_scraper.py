from scraper import Scraper

scraper = Scraper('https://www.google.com')
print('tag : {}'.format(scraper.tag_frequencies()))
print('tag text: {}'.format(scraper.tag_inner_text_frequencies()))
print('tag text words: {}'.format(scraper.tag_inner_text_words_frequencies()))
