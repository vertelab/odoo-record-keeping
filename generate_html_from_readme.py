#!/usr/bin/env python3

import os
from bs4 import BeautifulSoup
from docutils.core import publish_file
from pathlib import Path


def add_class(tag, class_name):
    """
    Recursively adds a class to a tag after deleting it if it exist
    """
    if tag.has_attr('class'):
        if class_name in tag['class']:
            del_class(tag, class_name)
            add_class(tag, class_name)
        else:
            tag['class'].append(class_name)
    else:
        tag['class'] = [class_name]


def del_class(tag, class_name):
    """
    Recursively deletes a class from a tag
    """
    if tag.has_attr('class'):
        if class_name in tag['class']:
            tag['class'].remove(class_name)
            del_class(tag, class_name)
        elif not tag['class']:
            del tag['class']


def modify4odoo_with_bs4(input):
    """
    Modifies input from rst file in order to make it look better in Odoo14/Module Info
    """
    soup = BeautifulSoup(input, 'html.parser')

    # Deletes styles as it has no impact in Odoo
    soup.find('style').extract()

    soup.find('div', class_='document')['class'].append('container')

    # Define html-tags to modify, check bootstrap 4.0 documentation
    tags = {
        'a': {'del': ['external', 'internal', 'reference', 'toc-backref']},
        'div': {'del': ['contents', 'document', 'local', 'section', 'topic']},
        'h1': {'add': ['border-bottom', 'mb-4', 'pb-2'], 'del': ['title']},
        'h2': {'add': ['pb-2']},
        'h3': {'add': ['my-3']},
        'li': {'add': ['my-2']},
        'p': {'add': ['mb-4']},
        'ul': {'add': ['mb-4'], 'del': ['simple']},
    }

    for tag_name in tags.keys():
        for tag in soup.find_all(tag_name):
            for class_name in tags[tag_name].get('add', []):
                add_class(tag, class_name)
            
            for class_name in tags[tag_name].get('del', []):
                del_class(tag, class_name)

    return soup


PATH = '/static/description/'
OUTPUT_FILENAME = 'index.html'

pathlist = Path(os.getcwd()).rglob('README.rst')

for pathitem in pathlist:
    destination = os.path.dirname(os.path.abspath(pathitem)) + PATH
    destination_path = destination + OUTPUT_FILENAME

    with open(os.path.abspath(pathitem), "r") as source:
        try:
            output = publish_file(
                destination_path=destination_path,
                source=source,
                writer_name='html')
            soup = modify4odoo_with_bs4(output)

        except Exception as error:
            print(error)

        with open(destination_path, 'wb') as file:
            try:
                file.write(soup.prettify('utf-8'))
                print('SUCCESS!', destination_path)

            except Exception as error:
                print('FAIL!', destination_path, error)

# from bs4 import BeautifulSoup

# with open("./Hämtningar/Klara_exempelfil_för_import.xml") as fp:  
#     soup = BeautifulSoup(fp, 'lxml') 
# for p in soup.find_all('process'):  
#     p_code = p.find('process.code').string.replace('.','_')
#     p_name = '"'+p.find('process.name').string+'"'
#     print(p_code, p_name) 
#     for q in p.find_all('processacttype'):
#         q_code = q.find('processacttype.sequence').string
#         q_name = '"'+q.find('processacttype.name').string+'"'
#         print(f"type_{q_code},classification_{p_code},{q_name}")
        