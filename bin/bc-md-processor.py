#!/usr/bin/env python3

__author__ = 'cjm'

import argparse
import logging
import yaml
from json import dumps

def main():

    parser = argparse.ArgumentParser(description='YAML tools for BioCaddie',
                                     formatter_class=argparse.RawTextHelpFormatter)


    subparsers = parser.add_subparsers(dest='subcommand', help='sub-command help')
    
    # SUBCOMMAND
    parser_n = subparsers.add_parser('validate', help='validate yml inside md')
    parser_n.set_defaults(function=validate_markdown)
    parser_n.add_argument('files', nargs='*')

    # SUBCOMMAND
    parser_n = subparsers.add_parser('concat', help='concat metadata yamls')
    parser_n.add_argument('-i', '--include', help='yml file to include for header')
    parser_n.add_argument('-o', '--output', help='output yaml')
    parser_n.add_argument('-c', '--context', help='jsonld context', default='biocaddie-context.jsonld')
    parser_n.set_defaults(function=concat_metadata_yaml)
    parser_n.add_argument('files',nargs='*')

    args = parser.parse_args()

    func = args.function
    func(args)


def validate_markdown(args):
    """
    Ensure the yaml encoded inside a YAML file is syntactically valid.

    First attempt to strip the yaml from the .md file, second use the standard python yaml parser
    to parse the embedded yaml. If it can't be passed then an error will be thrown and a stack
    trace shown. In future we may try and catch this error and provide a user-friendly report).
    
    In future we also perform additional structural validation on the yaml - check certain fields
    are present etc. This could be done in various ways, e.g. jsonschema, programmatic checks. We
    should also check translation -> jsonld -> rdf works as expected.
    """
    errs = []
    for fn in args.files:
        print("VALIDATING:"+fn)
        # we don't do anything with the results; an
        # error is thrown 
        (obj, md) = load_md(fn)
        print("OK:"+fn)
        errs += validate_structure(obj,md)
    if len(errs) > 0:
        print("FAILURES:")
        for e in errs:
            print("ERROR:"+e)
        exit(1)

def validate_structure(obj,md):
    errs = []
    #TODO put some biocaddie specific validation here
    return errs

def concat_metadata_yaml(args):
    """
    Given arguments with files and ouput,
    read YAML files into an array, decorate the objects, and write an output YAML file.
    Assumes that args.files is already sorted alphabetically.
    """
    objs = []
    foundry = []
    library = []
    obsolete = []
    cfg = {}
    ctxt = {}
    if (args.context):
        f = open(args.context, 'r')
        ctxt = yaml.load(f.read())
    if (args.include):
        f = open(args.include, 'r')
        cfg = yaml.load(f.read())
    for fn in args.files:
        (obj, md) = load_md(fn)
        if 'is_obsolete' in obj and obj['is_obsolete'] == True:
          obsolete.append(obj)
        elif 'in_foundry_order' in obj:
          foundry.append(obj)
        else:
          library.append(obj)
    objs = foundry + library + obsolete

    # hack 
    dateFields = ['date']
    for field in dateFields:
        for obj in objs:
            if field in obj:
                obj[field] = "date "+str(obj[field])

    cfg['datasets'] = objs
    if '@context' in ctxt:
        cfg['@context'] = ctxt['@context']
    f = open(args.output, 'w')
    f.write(dumps(cfg, sort_keys=True, indent=4, separators=(',', ': ')))
    #f.write(yaml.dump(cfg))
    return cfg


def concat_principles_yaml(args):
    objs = []
    cfg = {}
    if (args.include):
        f = open(args.include, 'r') 
        cfg = yaml.load(f.read())
    for fn in args.files:
        (obj, md) = load_md(fn)
        objs.append(obj)
    cfg['principles'] = objs
    f = open(args.output, 'w') 
    f.write(yaml.dump(cfg))
    return cfg


def load_md(fn):
    """
    Load a yaml text blob from a markdown file and parse the blob.

    Returns a tuple (yaml_obj, markdown_text)
    """
    f = open(fn, 'r') 
    text = f.read() 
    return extract(text)
    

def extract(mdtext):
    """
    Extract a yaml text blob from markdown text and parse the blob.

    Returns a tuple (yaml_obj, markdown_text)
    """
    lines = mdtext.split("\n")
    n = 0
    ylines = []
    mlines = []
    for line in lines:
        if (line == "---"):
            n=n+1
            hlines = []
        else:
            if (n == 1):
               ylines.append(line)
            else:
                mlines.append(line)
    yamltext = "\n".join(ylines)
    obj = yaml.load(yamltext)
    return obj, "\n".join(mlines)


if __name__ == "__main__":
    main()

    
    
