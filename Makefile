# This is a stub for now
test:
	echo ok

foo:
	echo $(GITHUB_TOKEN)

# Do a GitHub API query to fetch the locations of all repos with the biocaddie index tag
#
# Note you need a github token. Set either the environment var, or as a makefile var
# see also the samples/ directory for a sample.
#
# NOTE: if we instead place a magic token in the README, we can do a repo
# search instead, no API key required
#harvested-repos.json:
#	GITHUB_TOKEN=$(GITHUB_TOKEN) ./bin/harvest-github-metadata.sh > $@

# once the above is downloaded, iterate through the results and
# dump the MDs into the target/ directory
harvest: 
	./bin/harvester.py $<

# finally, iterate through all MDs and make a json-ld file and report file
harvested.json: 
	./bin/bc-md-processor.py concat target/*.md -o $@ > harvest.md
