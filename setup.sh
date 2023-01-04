#!/bin/bash
# This script will check whether Docker is available or not.
# If docker is available, it will check whearer a container named capital-gains
# exists and delete it. Afterwards it will build an image using the Dockerfile
# existing in the root of the project and add an alias to execute the CLI
# tool from within the container named capital-gains.

if [[ -x "$(command -v docker)" ]]; then
    if [[ $(docker ps -f ancestor=capital-gains -a | wc -l) -ge 2 ]]; then
        docker ps -f ancestor=cargo-events -a  --format "{{.ID}}" | xargs docker rm
    fi
    docker build --tag capital-gains .
    alias capital-gains="docker run --rm -i capital-gains"
else
    echo "docker not available"
    exit 1
fi