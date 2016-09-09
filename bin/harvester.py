#!/usr/bin/env python3

__author__ = 'cjm'

import argparse
import logging
import requests
from contextlib import closing

import sys
import yaml
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
    for fn in args.files:
        f = open(fn, 'r') 
        obj = json.load(f)
        f.close()
        for item in obj['items']:
            path = item['path']
            if path.startswith('_metadata'):
                repo = item['repository']
                reponame = repo['full_name']
                rawurl = 'https://raw.githubusercontent.com/' + reponame + '/gh-pages/' + path
                raws.append(rawurl)
                paths.append(path + reponame)
                with closing(requests.get(rawurl, stream=False)) as resp:
                    print("  Got response for: "+rawurl)
                    # TODO: redirects
                    ok = resp.status_code == 200
                    content = resp.text
                    fn = reponame + path
                    fn = 'target/' +  fn.replace('/','-')
                    print("SAVING TO "+fn)
                    f=open(fn,'w')
                    f.write(content)
                    print(content)
                    f.close()
            
                    sys.stdout.flush()



if __name__ == "__main__":
    main()

    
    
