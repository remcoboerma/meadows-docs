#!/bin/bash
# Backup documentation source files
set -e

BACKUP_DIR="backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

cp -r docs/ "$BACKUP_DIR/docs"
cp mkdocs.yml "$BACKUP_DIR/"
cp tasks.py "$BACKUP_DIR/"
cp docker-compose.yml "$BACKUP_DIR/"
cp Dockerfile* "$BACKUP_DIR/"
cp app.py "$BACKUP_DIR/"

echo "Backup created in $BACKUP_DIR"
