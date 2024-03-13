# bin/bash

vendor/bin/arche-crawl-meta \
  rdf \
  rdf/metadata.ttl \
  /data \
  https://id.acdh.oeaw.ac.at/auden-musulin-papers \
  --repositoryUrl https://arche.acdh.oeaw.ac.at/api/ \
  --logFile ./rdf/crawl.log