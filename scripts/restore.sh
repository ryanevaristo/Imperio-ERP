#!/bin/bash
# ── Restore do PostgreSQL — Alicerce ───────────────────────────────────────
# Uso: bash scripts/restore.sh /backups/alicerce_20240101_120000.sql.gz
# ──────────────────────────────────────────────────────────────────────────────

set -e

BACKUP_FILE="$1"

if [ -z "${BACKUP_FILE}" ]; then
    echo "Uso: bash scripts/restore.sh <arquivo_backup.sql.gz>"
    echo "Backups disponíveis em /backups/:"
    ls -lh /backups/alicerce_*.sql.gz 2>/dev/null || echo "  (nenhum backup encontrado)"
    exit 1
fi

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Erro: arquivo '${BACKUP_FILE}' não encontrado."
    exit 1
fi

DB_HOST="${POSTGRES_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-postgres}"
DB_USER="${POSTGRES_USER:-postgres}"
PGPASSWORD="${POSTGRES_PASSWORD:-postgres}"
export PGPASSWORD

echo "[$(date)] ATENÇÃO: Isso vai sobrescrever o banco '${DB_NAME}' em ${DB_HOST}."
read -p "Confirmar restore? (s/N): " CONFIRM
if [ "${CONFIRM}" != "s" ] && [ "${CONFIRM}" != "S" ]; then
    echo "Restore cancelado."
    exit 0
fi

echo "[$(date)] Iniciando restore de: ${BACKUP_FILE}"

gunzip -c "${BACKUP_FILE}" | psql \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    "${DB_NAME}"

echo "[$(date)] Restore concluído com sucesso!"
