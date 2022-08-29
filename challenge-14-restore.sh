#!/bin/bash

#DATE=$(date +%Y-%m-%d-%H-%M)
DATADIR=/home/nearval/neardata
BACKUPDIR=${DATADIR}/backups

NEWEST=$(ls -t $BACKUPDIR/data_* | head -1)

sudo systemctl stop neard

wait

echo "NEAR node was stopped" | ts

if [ -d "$BACKUPDIR" ]; then
    echo "Starter started" | ts

    rm -rf $DATADIR/.near/data/*

    unzip ${NEWEST} -d $DATADIR/.near/data/

    echo "Databack restored from ${NEWEST}" | ts
else
    echo $BACKUPDIR is not created. Check your permissions.
    exit 0
fi

sudo systemctl start neard

echo "NEAR node was started" | ts
