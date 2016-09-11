#!/usr/bin/env python3

__author__ = 'cjm'

import argparse
import logging
import requests
from contextlib import closing

import sys
import json

blacklist = ['my-first-dataset', 'my-second-dataset']

# curl -H "Authorization: token $GITHUB_TOKEN" 'https://api.github.com/search/code?q="index%3A+biocaddie"'

params = {
    'access_token' : ''
    }

def main():

    parser = argparse.ArgumentParser(description='harvester'
                                                 'Harvests MD-YAML files using github search results',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('files',nargs='*')
    parser.add_argument('-r', '--report', type=str, default='report.md')
    parser.add_argument('-k', '--key' ,type=str)


    args = parser.parse_args()

    params['access_token'] = args.key

    paths = []
    raws = []
    travisurls = []

    # find all repos with magic token
    repos = search_repos()
    for repo in repos:
        travisurl = 'https://travis-ci.org/' + repo
        
        # find all md files within repo
        urls = get_md_urls(repo)

        # iterate through md urls, downloading each
        n = 0
        for url in urls:
            print("Checking:"+url)
            skip = false;
            for bn in blacklist:
                if url.find(bn) > -1:
                    print("Skipping: "+url)
                    skip = true
            if skip:
                continue
            #travisurls.append(travisurl)
            with closing(requests.get(url, params, stream=False)) as resp:
                print("  Status of "+url+" = "+str(resp.status_code))
                ok = resp.status_code == 200
                content = resp.text
                fn = url.replace('https://raw.githubusercontent.com/',"")
                fn = 'target/' +  fn.replace('/','-')
                f=open(fn,'w')
                f.write(content)
                f.close()
                n=n+1
        if n > 0:
            travisurls.append(travisurl)

    f=open(args.report,'w')
    for url in travisurls:
        f.write(' * [![Build Status](%s.svg?branch=gh-pages)](%s) %s' % (url,url,url))
        f.write("\n")
    f.close()

def search_repos():
    url = 'https://api.github.com/search/repositories?q=biocaddie+in:readme+fork:true'
    names = []
    with closing(requests.get(url, params, stream=False)) as resp:
        ok = resp.status_code == 200
        if ok:
            content = resp.text
            results = json.loads(content)
            items = results['items']
            for item in items:
                full_name = item['full_name']
                names.append(full_name)
        else:
            print("oops: "+url + "\n" + resp.text)            
    return names
    
def get_md_urls(repo):
    url = 'https://api.github.com/repos/'+repo+'/contents/_metadata?ref=gh-pages'
    urls = []
    with closing(requests.get(url, params, stream=False)) as resp:
        ok = resp.status_code == 200
        if ok:
            print("Fetching files from "+url)
            content = resp.text
            results = json.loads(content)
            for item in results:
                urls.append(item['download_url'])
        else:
            print("oops: "+url + "\n" + resp.text)
    return urls
            
            
        
if __name__ == "__main__":
    main()

    
    
