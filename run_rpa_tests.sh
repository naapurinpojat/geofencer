#!/bin/bash
docker run --network=snowdog_mynetwork -it --rm -v $(pwd):/tests snowdog-rpa-snowdog bash -c "robot --outputdir ./tests/tests/results /tests"
