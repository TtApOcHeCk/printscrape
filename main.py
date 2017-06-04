# -*- coding: utf-8 -*-
import os
import random
import requests
import argparse
import threading
import cfscrape
import string
import re

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--threads', type=int, default=5, help='sets the number of threads')
namespace = parser.parse_args()

base_file = 'used.txt'
img_dir = 'img'
scraper = cfscrape.create_scraper()
if not os.path.exists(base_file):
    open(base_file, 'a').close()
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

def main():
    initial_url = get_string()
    full_url = 'http://prnt.sc/' + initial_url
    print('[*] processing link {}'.format(full_url))
    image_link = get_img_link(full_url)
    if image_link:
        print('[+] image found {}'.format(image_link))
        save_img(initial_url, image_link)
    else:
        print('[-] bad luck, moving on')

def get_string():
    initial_symbol = list(string.digits + string.ascii_lowercase[:6])#6 #first symbol rules: [0-9a-f] (others haven't been uploaded yet)
    other_symbols = list(string.digits + string.ascii_lowercase) #other five symbols: [0-9a-z]
    basefile = open(base_file, 'r')
    base = [item.strip() for item in basefile]
    basefile.close()
    while True:
        final_string = str()
        final_string += initial_symbol[random.randint(0, len(initial_symbol)-1)] 
        for i in range(5):
            final_string += other_symbols[random.randint(0,len(other_symbols)-1)] 
        if final_string not in base:
            write_to_base(final_string)
            return final_string
    
def write_to_base(link):
    with open('used.txt', 'a') as base_file:
        base_file.write(link + '\n')

def get_img_link(link):
    html_response = str(scraper.get(link).content)
    native_img = re.search(r'http://image.prntscr.com/image/\w+.png', html_response)
    imgur_img = re.search(r'http://i.imgur.com/\w+.png', html_response)
    if (native_img or imgur_img):
        return (native_img or imgur_img).group()

def save_img(initial_url, img_link):
    img = requests.get(img_link)
    with open('{0}/{1}.png'.format(img_dir, initial_url), 'wb') as file:
        file.write(img.content)
def loop():
    while True:
        main()

threads = {}
for i in range(namespace.threads):
    threads[i] = threading.Thread(target=loop)
    threads[i].start()
