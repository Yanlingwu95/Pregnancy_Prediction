#!/bin/bash


echo "export NDGRID_API_KEY='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'" > sendgrid.env

echo "sendgrid.env" >> .gitignore

source ./sendgrid.env

echo "Setup the send email environment successfully"

exit 0
