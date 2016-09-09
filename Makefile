# This is a stub for now
test:
	echo ok

foo:
	echo $(GITHUB_TOKEN)

# Do a GitHub API query to fetch the locations of all repos with the biocaddie index tag
#
# Note you need a github token. Set either the environment var, or as a makefile var
# see also the samples/ directory for a sample
harvested-repos.json:
	GITHUB_TOKEN=$(GITHUB_TOKEN) ./bin/harvest-github-metadata.sh > $@

# once the above is downloaded,
harvest: harvested-repos.json
	./bin/harvester.py $<

harvested.json: 
	./bin/bc-md-processor.py concat target/*.md -o $@
