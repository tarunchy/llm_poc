#!/bin/bash

if [ -f app_id ]; then
    kill $(cat app_id)
    rm app_id
    echo "Application stopped."
else
    echo "No running application found."
fi

# Deactivate the virtual environment
#source env/bin/deactivate

