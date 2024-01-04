#!/bin/bash
NETNAME=$(basename $(pwd))
docker run --network=${NETNAME}_mynetwork -it --rm -v $(pwd):/tests snowdog-rpa-snowdog bash -c "robot --outputdir ./tests/tests/results /tests"
