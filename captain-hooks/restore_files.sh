#!/bin/bash
# Restore documentation source files from backup
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_dir>"
    echo "Available backups:"
    ls -d backup/*/ 2>/dev/null || echo "  No backups found"
    exit 1
fi

BACKUP_DIR="$1"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backup directory not found: $BACKUP_DIR"
    exit 1
fi

cp -r "$BACKUP_DIR/docs" ./
cp "$BACKUP_DIR/mkdocs.yml" ./
cp "$BACKUP_DIR/tasks.py" ./
cp "$BACKUP_DIR/docker-compose.yml" ./
cp "$BACKUP_DIR/Dockerfile"* ./
cp "$BACKUP_DIR/app.py" ./

echo "Restored from $BACKUP_DIR"
