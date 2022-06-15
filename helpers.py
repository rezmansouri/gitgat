import os
import re
from urllib import request as req, parse
from shutil import make_archive, rmtree
from bs4 import BeautifulSoup

github_file_root = 'https://raw.githubusercontent.com'
github_dir_root = 'https://github.com/'
file_css_tag = 'js-navigation-open Link--primary'
storage_address = 'storage/'


def crawl(url: str, dir_name):
    """
    this is a recursive function.
    it receives a directory url and looks into the directory.
    if a directories is found within, it is crawled again, otherwise the file will be downloaded.
    """
    os.mkdir(storage_address + dir_name)
    page = req.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    url_elements = soup.find_all('a', class_=file_css_tag)
    for url_element in url_elements:
        url_ = url_element.attrs['href']
        base_name = parse.unquote(os.path.basename(url_))
        if url_.__contains__('/blob/'):
            file_url = github_file_root + url_.replace('/blob/', '/')
            req.urlretrieve(file_url, storage_address + dir_name + '/' + base_name)
        else:
            crawl(github_dir_root + url_, f'{dir_name}/{base_name}')


def clear_storage(dir_name):
    os.remove(f'{storage_address}{dir_name}.zip')
    rmtree(f'{storage_address}{dir_name}')


def validate_url(url: str):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
    if re.search('https?://github.com(/[^/].*){2,}', url) is None:
        return False, False
    dir_name = parse.unquote(parse.unquote(url.split('/')[-1]))
    return url, dir_name + '.zip'
