#!/usr/bin/env python3

__author__ = 'cjm'

import argparse
import logging
import requests
from contextlib import closing

import sys
import json

# curl -H "Authorization: token $GITHUB_TOKEN" 'https://api.github.com/search/code?q="index%3A+biocaddie"'


def main():

    parser = argparse.ArgumentParser(description='harvester'
                                                 'Harvests MD-YAML files using github search results',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('files',nargs='*')

    args = parser.parse_args()

    paths = []
    raws = []
    travisurls = []
    
    repos = search_repos()
    for repo in repos:
        travisurl = 'https://travis-ci.org/' + repo
        
        urls = get_md_urls(repo)
        if len(urls) > 0:
            travisurls.append(travisurl)

        for url in urls:
            #travisurls.append(travisurl)
            with closing(requests.get(url, stream=False)) as resp:
                #print("  Got response for: "+rawurl)
                # TODO: redirects
                ok = resp.status_code == 200
                content = resp.text
                fn = url.replace('https://raw.githubusercontent.com/',"")
                fn = 'target/' +  fn.replace('/','-')
                #print("SAVING TO "+fn)
                f=open(fn,'w')
                f.write(content)
                #print(content)
                f.close()

    f=open('report.md','w')
    for url in travisurls:
        f.write(' * [![Build Status](%s.svg?branch=gh-pages)](%s)' % (url,url))
        f.write("\n")
    f.close()

def search_repos():
    url = 'https://api.github.com/search/repositories?q=biocaddie+in:readme+fork:true'
    names = []
    with closing(requests.get(url, stream=False)) as resp:
        ok = resp.status_code == 200
        content = resp.text
        results = json.loads(content)
        items = results['items']
        for item in items:
            full_name = item['full_name']
            names.append(full_name)
            
    return names
    
def get_md_urls(repo):
    url = 'https://api.github.com/repos/'+repo+'/contents/_metadata?ref=gh-pages'
    urls = []
    with closing(requests.get(url, stream=False)) as resp:
        ok = resp.status_code == 200
        if ok:
            print("Fetching files from "+url)
            content = resp.text
            results = json.loads(content)
            for item in results:
                urls.append(item['download_url'])
        else:
            print("oops: "+url)
    return urls
            
            
        
if __name__ == "__main__":
    main()

    
    
