#!/bin/bash

source alice-production-db
source brandy-production-db

gcloud beta sql backups restore $ALICE --restore-instance=alice-production-db-clone --backup-instance=alice-production-db -q
gcloud beta sql backups restore $BRANDY --restore-instance=brandy-production-db-clone --backup-instance=brandy-production-db -q