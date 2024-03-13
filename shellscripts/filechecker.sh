# bin/bash

# docker run \
#     --name filechecker \
#     --rm \
#     -v `pwd`/filechecker/reports:/reports \
#     -v /mnt/acdh_resources/container/R_amp_19479/600_imgs_tiff/imgs_auden:/data \
#     -v ~/.cvdupdate/database/:/var/lib/clamav \
#     acdhch/arche-filechecker

docker run \
    --name filechecker \
    --rm \
    -v `pwd`/filechecker/reports:/reports \
    -v ./data:/data \
    -v ~/.cvdupdate/database/:/var/lib/clamav \
    acdhch/arche-filechecker

filelist_path=$(find ./filechecker/reports -name "fileList.json")
echo "Filelist path: $filelist_path; moving to rdf folder"
cp $filelist_path ./rdf/fileList.json
sed -i -e s/\\/metadata/''/g -e s/\\/editions/''/g -e s/\\/indexes/''/g ./rdf/fileList.json

# docker run \
#     --name metadataCrawler \
#     --rm \
#     -v ./rdf:/data \
#     -v `pwd`/to_ingest:/to_ingest \
#     /data \
#     /to_ingest/metadata.ttl \
#     /data \
#     https://id.acdh.oeaw.ac.at/auden-musulin-papers \
#     acdhch/arche-metadata-crawler
