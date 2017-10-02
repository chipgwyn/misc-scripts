#!/usr/bin/env python3

import re
# import pickle
from bs4 import BeautifulSoup
from shutil import copyfile
from jinja2 import FileSystemLoader, Environment

env = Environment(loader=FileSystemLoader('.'))

page_template = env.get_template('page.tmpl')
html_doc = open('html/My Library _ Audible.com.html')
soup = BeautifulSoup(html_doc, 'html.parser')


# Generate a list of titles and their direct audible.com urls
links = {}
for book_link in soup.find_all('a', {'class':
                                     'adbl-flyout-trigger-marker adbl-link adbl-prod-title adbl-series-margin-bottom'}):
    url = book_link.attrs['href']
    title = book_link.get_text()
    links[title] = url


# Find all the images for each book
images = {}
for image in soup.find_all('img', {'class': 'adbl-prod-image'}):
    img_url = image.attrs['src']
    img_url = img_url.split('/')[-1]
    # print(image.attrs['src'])
    file_name = image.attrs['src'].split('/')[-1]
    alt_text = image.attrs['alt']
    # print(alt_text)
    images[alt_text] = img_url
    copyfile('html/' + image.attrs['src'], 'site/images/' + file_name)


# Find all Table Data Columns with class="adbl-flyout-cont-marker" and name="productCover"
info = {}
by_re = re.compile(r'^(By|Narrated By)\s')
for ds in soup.find_all('td', {'class': 'adbl-flyout-cont-marker', 'name': 'productCover'}):
    for div in ds.find_all('div', {'class': 'socialTile-summary'}):
        title = ''
        author = ''
        narrator = ''
        # We don't care about this specific crap...
        if 'Vango' in div.text:
            continue
        if 'Your First Listen' in div.text:
            continue
        if 'The New York Times Audio Digest' in div.text:
            continue

        # Find the author, surrounded with 'h3' tag
        if len(div.find('h3').get_text()) > 1:
            title = div.find('h3').get_text()
            # print(div.find('h3').get_text())

            # The title of the book matches what we found in the links previously, include the link in our new
            # consolidated info dict
            info[title] = {}
            if title in links.keys():
                info[title]['url'] = links[title]

            # The title of the book matches what we found in the images previously, include them in our new dict
            if title in images.keys():
                info[title]['image'] = images[title]

        # Add the author and narrator to our info dict
        if len(div.find_all('li')) > 2:
            author = div.find_all('li')[1].get_text()
            info[title]['author'] = re.sub(by_re, '', author)
            narrator = div.find_all('li')[2].get_text()
            info[title]['narrator'] = re.sub(by_re, '', narrator)


# Print out all our data!
# print('-' * 40)
# by_re = re.compile(r'^(By|Narrated By)\s')
# for k, v in info.items():
#     print('Title: {}'.format(k))
#     for k2, v2 in v.items():
#         print('{}: {}'.format(k2, re.sub(by_re, '', v2)))
#     print('-' * 40)


# close our open file handle
html_doc.close()

# pickle.dump(info, open('info.pickle', 'wb'))
# info = pickle.load(open('info.pickle', 'rb'))

# s = sorted(info.items(), key=lambda x: (x[0].split(': ')[-1], x[0].split(', ')[-1] ))
# for item in s:
#     print(item[0])


with open('site/html/index.html', 'w') as index:
    index.write(page_template.render(data=sorted(info.items(), key=lambda x: (x[0].split(': ')[-1], x[0].split(', ')[-1]))))
