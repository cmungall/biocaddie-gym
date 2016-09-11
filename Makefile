all: rdf/aggregated-metadata.ttl

# This is a stub for now
test:
	echo ok

foo:
	echo $(GITHUB_TOKEN)

# 1. Do a GitHub API query to fetch the locations of all repos with the biocaddie index tag
# 2. Iterate through results, copying source md file into target/ dir
harvest: 
	./bin/harvester.py -k $(GITHUB_TOKEN) $<

# after harvest,
# iterate through all MDs and make a json-ld file and report file
aggregated-metadata.jsonld: 
	./bin/bc-md-processor.py concat target/*.md -o $@ -r key-report.json

rdf/%.ttl: %.jsonld
	riot $< > $@.tmp && mv $@.tmp $@

# warning: hardcodes assumptions about directory layout
sync:
	cp target/*.md ../mybiocaddie-aggregator/_metadata


## ----------------------------------------
## LOADING BLAZEGRAPH
## ----------------------------------------

BGJAR = jars/blazegraph.jar

$(BGJAR):
	mkdir -p jars && cd jars && curl -O http://tenet.dl.sourceforge.net/project/bigdata/bigdata/2.1.1/blazegraph.jar
.PRECIOUS: $(BGJAR)

BG = java -XX:+UseG1GC -Xmx12G -cp $(BGJAR) com.bigdata.rdf.store.DataLoader -defaultGraph http://geneontology.org/rdf/ conf/blazegraph.properties
load-blazegraph: $(BGJAR)
	$(BG) rdf

rmcat:
	rm rdf/catalog-v001.xml

rdf/%-bg-load: rdf/%.rdf
	$(BG) $<

bg-start:
	java -server -Xmx8g -Dbigdata.propertyFile=conf/blazegraph.properties -jar $(BGJAR)
