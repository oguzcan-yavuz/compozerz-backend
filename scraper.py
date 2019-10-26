from urllib.parse import urljoin
from urllib.request import urlopen
import time
import os
import re
from bs4 import BeautifulSoup
import constants as Constants


def scrape_composer_from_midiworld(composer):
    url = urljoin(Constants.MIDIWORLD_URL, "{0}.{1}".format(composer.lower(), "htm"))
    response = urlopen(url)
    html = response.read()
    return html


def is_midi_extension(s):
    return s.endswith(".mid")


def get_all_links_from_page(page):
    soup = BeautifulSoup(page, "html.parser")
    parsed_links = [link["href"] for link in soup.find_all("a")]
    return parsed_links


def scrape_midis_of_composer(composer):
    print("scraping midi urls of composer: {0}".format(composer))
    page = scrape_composer_from_midiworld(composer)
    links = get_all_links_from_page(page)
    midi_links = [link for link in links if is_midi_extension(link)]
    print("scraped midi link count for {0} is: {1}".format(composer, len(midi_links)))
    return midi_links


def get_midi_name_from_url(url):
    return url.split("/")[-1]


def create_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_dirs_for_composer(composer):
    composer_path = os.path.join(Constants.DATA_PATH, composer.lower(), "midi")
    create_dirs(composer_path)
    return composer_path


def get_midis_of_composer(composer):
    midi_urls = scrape_midis_of_composer(composer)
    for url in midi_urls:
        midi_name = get_midi_name_from_url(url)
        composer_path = create_dirs_for_composer(composer)
        midi_path = os.path.join(composer_path, midi_name)
        print("downloading midi: {}".format(midi_name))
        urllib.request.urlretrieve(url, midi_path)


def main():
    for composer in Constants.COMPOSER_NAMES:
        get_midis_of_composer(composer)
    print("All is done!")


main()
