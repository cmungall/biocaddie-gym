# This is a stub for now
test:
	echo ok

foo:
	echo $(GITHUB_TOKEN)

# Note you need a github token. Set either the environment var, or as a makefile var
harvest.json:
	GITHUB_TOKEN=$(GITHUB_TOKEN) ./bin/harvest-github-metadata.sh > $@
