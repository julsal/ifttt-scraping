import os
from selenium.webdriver.common.by import By

from mysl.scraper import MyslBrowserScraper
import mysl.file_reader as fr
import turk


def download(urls, basedir):
    print('Downloading {} urls to save in "{}".'.format(len(urls), basedir))
    scraper = MyslBrowserScraper()

    for i, url in enumerate(urls):
        print('downloading "{}" ({} out of {})...'.format(url, str(i + 1), len(urls)))
        file_name = os.path.join(basedir, url.replace('https://ifttt.com/recipes/', ''))
        scraper.save_in_file(url, file_name)

    scraper.close()
    print("END!")


def run():
    # urls_file = '/home/juliano/git/ifttt-quirk/data/all.urls'
    ##urls = fr.line_to_list(urls_file)
    gold = '/home/juliano/Documents/phd/commands/ifttt-recipes/content.tsv'
    gold_tuples = fr.line_to_tuple_in_list(gold, separator='\t', ignore_headline=True)
    gold_dict = dict()
    for g in gold_tuples:
        gold_dict['https://ifttt.com/recipes/' + g[turk.URL]] = g

    urls = turk.get_relevant_urls(majority=False, gold=gold_dict)
    print('total: ' + str(len(urls)))
    basedir = '/home/juliano/Documents/phd/commands/ifttt-recipes/relevant'


    #download(urls, basedir)


run()
