sudo docker run \
    --name filechecker \
    --rm \
    -v `pwd`/filechecker/reports:/reports \
    -v `pwd`/data:/data \
    -v ~/.cvdupdate/database/:/var/lib/clamav \
    acdhch/arche-filechecker