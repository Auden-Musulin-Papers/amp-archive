docker run \
  --rm \
  -ti \
  --name arche-ingest \
  -v ./rdf:/data \
  acdhch/arche-ingest