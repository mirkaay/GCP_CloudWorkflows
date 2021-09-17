#!/bin/sh
# [START startup_script]
sudo apt-get update -y
HOSTNAME=$(hostname)
# TIME=$(date +%T)
TIME=$(date -d '+ 5 minutes'  '+%FT%T.000Z')
gcloud scheduler jobs create pubsub $HOSTNAME --schedule="*/4 * * * *" --topic=delete-my-vm --message-body="Deleting VM" --attributes="virtualmachine=$HOSTNAME, time=$TIME"
# gcloud projects add-iam-policy-binding <PROJECT ID> --member='user:<USER EMAIL>' --role='projects/<PROJECT ID>/roles/<ROLE NAME>' --condition='expression=request.time < timestamp("'$TIME'"),title=expires_end_of_2021,description=Expires at midnight on 2021-12-31'

