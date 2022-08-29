#!/bin/bash

DATE=$(date +%Y-%m-%d-%H-%M)
DATADIR=/home/nearval/neardata
BACKUPDIR=${DATADIR}/backups

mkdir -p $BACKUPDIR

OLDEST=$(ls -t $BACKUPDIR/data_* | tail -1)

sudo systemctl stop neard

wait

echo "NEAR node was stopped" | ts

if [ -d "$BACKUPDIR" ]; then
    echo "Backup started" | ts

    zip -j ${BACKUPDIR}/data_${DATE}.zip $DATADIR/.near/data/*

    echo "Backup completed ${BACKUPDIR}/data_${DATE}.zip" | ts

    rm ${OLDEST}

    echo "oldest file deleted ${OLDEST}" | ts
else
    echo $BACKUPDIR is not created. Check your permissions.
    exit 0
fi

sudo systemctl start neard

echo "NEAR node was started" | ts
