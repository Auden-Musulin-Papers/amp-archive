# bin/bash

echo "add attributes"
add-attributes -g "./data/indexes/*.xml" -b "https://id.acdh.oeaw.ac.at"
add-attributes -g "./data/editions/*.xml" -b "https://id.acdh.oeaw.ac.at"