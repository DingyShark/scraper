#!/usr/bin/env python3
import os
import requests
import re
from colorama import Fore, Style, init
from argparse import ArgumentParser
import sys


# Download all [extensions] links from file that contains urls
def extensions_downloader(input_path ,output_path):
    with open(input_path, 'r', encoding="utf8") as url_file:
        for url in url_file:
            url = url.strip()
            # Check, if link contains [extensions]
            if url.split('.')[-1] in extensions:
                with open(fr'{output_path}\{url.split("/")[-1]}', 'w', encoding='utf-8') as file:
                    # Get request of that link and save results
                    file.write(requests.get(url).text)
                    print(Fore.GREEN+'[+]  File:', url.split("/")[-1], 'successfully downloaded', Style.RESET_ALL)
            else:
                continue


# Find all comments in single file
def comments_finder(ext_file):
    with open(ext_file, 'r', encoding="utf8") as file:
        print(Fore.GREEN+'[+]  Searching comments in file', ext_file.split('\\')[-1], Style.RESET_ALL)
        for word in file:
            # Regex for comments
            if re.findall(r'(//.*)|(\*.*)|(<!--([\s\S]*?)-->)', word):
                print(word.strip())
            else:
                continue


# Find all [interesting_words] in single file
def interesting_words_finder(ext_file):
    # Find only unique items
    unique_items = set()
    with open(ext_file, 'r', encoding="utf8") as file:
        print(Fore.GREEN+'[+]  Searching interesting words in file', ext_file.split('\\')[-1], Style.RESET_ALL)
        for word in file:
            for interesting_word in interesting_words:
                # Check if file's line contains [interesting_words], if so, add to unique items
                if interesting_word in word:
                    unique_items.add(Fore.RED+interesting_word+': '+Style.RESET_ALL+word.strip())
                else:
                    continue
    # Print all unique items
    for item in unique_items:
        print(item)


# Find possible hashes or jwt in single file
def hashes_and_jwt_finder(ext_file):
    with open(ext_file, 'r', encoding="utf8") as file:
        print(Fore.GREEN + '[+]  Searching hashes/jwt tokens in file', ext_file.split('\\')[-1], Style.RESET_ALL)
        for word in file:
            # Regex for hash and jwt
            if re.findall(r'([A-Fa-f0-9]{32,})|(eyJ)', word):
                print(word.strip())
            else:
                continue


if __name__ == '__main__':
    init()
    extensions = ['js', 'html']
    interesting_words = ['passwords', 'secretkey', 'admin', 'secret', 'apikey', 'user', 'username', 'token', 'accesstoken', 'jwt', 'hash']

    # Available arguments(in cmd type -h for help)
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', help="Input file with urls contains JS and HTML content to download /home/kali/urls.txt", default='')
    parser.add_argument('-o', '--output', help="Output path, to save JS and HTML content(default current directory) /home/kali/extensions", default=os.getcwd())
    parser.add_argument('-f', '--file', help="JS or HTML file for analysis /home/kali/extensions/some_js.js", default='')
    parser.add_argument('-c', '--comments', help="Find all comments", action='store_true')
    parser.add_argument('-w', '--words', help=f"Find all interesting words from the list:{interesting_words}", action='store_true')
    parser.add_argument('-hj', '--hashes_and_jwt', help="Find all hashes or/and jwt", action='store_true')
    parser.add_argument('-a', '--all', help="Find all", action='store_true')
    args = parser.parse_args()

    # Find content in file
    if args.file != '':
        try:
            if args.comments:
                comments_finder(args.file)
            if args.words:
                interesting_words_finder(args.file)
            if args.hashes_and_jwt:
                hashes_and_jwt_finder(args.file)
            if args.all:
                comments_finder(args.file)
                interesting_words_finder(args.file)
                hashes_and_jwt_finder(args.file)
        except FileNotFoundError:
            print(Fore.RED+'[!]  Not existing file or path'+Style.RESET_ALL)
    # Download all [extensions] links from file that contains urls
    elif args.input != '' and args.output != '':
        try:
            extensions_downloader(args.input, args.output)
        except FileNotFoundError:
            print(Fore.RED+'[!]  Not existing file or path'+Style.RESET_ALL)
    else:
        parser.print_help()
        sys.exit(1)
