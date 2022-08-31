#!/bin/bash


STAKE=$(near validators current | grep markelov | cut -d '|' -f3)

echo "STAKE $STAKE" | ts

npm run --prefix dev/notifi-sdk-ts/packages/notifi-node-sample mes -- $STAKE


echo "message sent" | ts
