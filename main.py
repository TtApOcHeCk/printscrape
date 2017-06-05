# -*- coding: utf-8 -*-
import os
import sys
import random
import string
import requests
import argparse
import threading
import cfscrape
import string
import re

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--threads', type=int, default=5, help='sets the number of threads')
parser.add_argument('-c', '--charset', default=None, help='sets a character mask for links generating, see README.md for syntax information')
namespace = parser.parse_args()

base_file = 'used.txt'
img_dir = 'img'
charset_values = {'?d': string.digits, '?s': string.ascii_lowercase, '?a': string.digits + string.ascii_lowercase}
scraper = cfscrape.create_scraper()
if not os.path.exists(base_file):
    open(base_file, 'a').close()
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

def main():
    initial_url = get_string(namespace.charset)
    full_url = 'http://prnt.sc/' + initial_url
    print '[*] processing link {}'.format(full_url)
    image_link = get_img_link(full_url)
    if image_link:
        print '[+] image found {}'.format(image_link)
        save_img(initial_url, image_link)
    else:
        print '[-] bad luck, moving on'

def get_string(mask):
    basefile = open(base_file, 'r')
    base = [item.strip() for item in basefile]
    basefile.close()
    while True:
        final_string = generate_string(mask) 
        if final_string not in base:
            write_to_base(final_string)
            return final_string
        
def generate_string(mask):
    random_string = str()
    if mask:
        input_charset = re.findall(r'{([^\{\}]+)}', mask)
        for symbol in input_charset:
            if symbol in charset_values:
                random_string += charset_values[symbol][random.randint(0,len(charset_values[symbol])-1)]
            else:
                letters = re.findall(r'([a-z]-[a-z]|[a-z])', symbol)
                numbers = re.findall(r'([0-9]-[0-9]|[0-9])', symbol)
                specific_charset = ''
                if letters:
                    letters = letters[0].split('-')
                    specific_charset += charset_values['?s'][charset_values['?s'].index(letters[0]):charset_values['?s'].index(letters[::-1][0])+1]
                if numbers:
                    numbers = numbers[0].split('-')
                    specific_charset += charset_values['?d'][charset_values['?d'].index(numbers[0]):charset_values['?d'].index(numbers[::-1][0])+1]
                random_string += specific_charset[random.randint(0, len(specific_charset)-1)]
        random_string = random_string[:6]
    while len(random_string) < 6:
        random_string += charset_values['?a'][random.randint(0,len(charset_values['?a'])-1)]
    return random_string
    
def write_to_base(link):
    with open('used.txt', 'a') as base_file:
        base_file.write(link + '\n')

def get_img_link(link):
    html_response = scraper.get(link).content
    native_img = re.search('http[s]*://image.prntscr.com/image/\w+.png', html_response)
    imgur_img = re.search('http[s]*://i.imgur.com/\w+.png', html_response)
    if (native_img or imgur_img):
        return (native_img or imgur_img).group()

def save_img(initial_url, img_link):
    img = requests.get(img_link)
    with open('{0}/{1}.png'.format(img_dir, initial_url), 'wb') as file:
        file.write(img.content)

def loop():
    while True:
        try:
            main()
        except KeyboardInterrupt:
            sys.exit()

threads = {}
for i in range(namespace.threads):
    threads[i] = threading.Thread(target=loop)
    threads[i].start()
