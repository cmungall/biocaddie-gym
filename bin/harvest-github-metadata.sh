#!/bin/sh
curl -H "Authorization: token $GITHUB_TOKEN" 'https://api.github.com/search/code?q="index%3A+biocaddie"+in%3Afork'
