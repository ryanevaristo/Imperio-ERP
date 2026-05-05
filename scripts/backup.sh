#!/bin/bash
# ── Backup automático do PostgreSQL — Imperio ERP ──────────────────────────────
# Uso manual:  bash scripts/backup.sh
# Em produção: executado diariamente pelo serviço 'backup' no docker-compose.yml
# ──────────────────────────────────────────────────────────────────────────────

set -e

BACKUP_DIR="/backups"
DB_HOST="${POSTGRES_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-postgres}"
DB_USER="${POSTGRES_USER:-postgres}"
PGPASSWORD="${POSTGRES_PASSWORD:-postgres}"
KEEP_DAYS="${BACKUP_KEEP_DAYS:-30}"   # Mantém últimos 30 dias de backup

export PGPASSWORD

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="${BACKUP_DIR}/imperio_erp_${TIMESTAMP}.sql.gz"

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Iniciando backup: ${FILENAME}"

pg_dump \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    "${DB_NAME}" | gzip > "${FILENAME}"

echo "[$(date)] Backup concluído: ${FILENAME} ($(du -h "${FILENAME}" | cut -f1))"

# Remove backups mais antigos que KEEP_DAYS dias
find "${BACKUP_DIR}" -name "imperio_erp_*.sql.gz" -mtime "+${KEEP_DAYS}" -delete
echo "[$(date)] Backups antigos (>${KEEP_DAYS} dias) removidos."
