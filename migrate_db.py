"""Create and update the database schema used by the application.

This script is intentionally idempotent: it can be run after every deploy.
Create a database backup before running it in a production environment.
Usage: python migrate_db.py
"""

import sys

from sqlalchemy import inspect, text

from app import app
from models import db


LEGACY_ATENDENTE_BACKUP = 'atendente_legacy'
SETORES_PADRAO = [
    'Atenção Primária',
    'CAF',
    'CPD',
    'Fundo Municipal',
    'Gabinete Executivo',
    'Planejamento',
    'PNI',
    'Regulação',
    'RH',
    'SAES',
    'T.I.',
    'Vigilância Epidemiológica',
    'ViSa',
]


def column_names(inspector, table_name):
    return {column['name'] for column in inspector.get_columns(table_name)}


def add_column_if_missing(connection, inspector, table_name, column_name, definition):
    columns = column_names(inspector, table_name)
    if column_name in columns:
        return False

    connection.execute(text(
        f'ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {definition}'
    ))
    inspector.clear_cache()
    print(f'Coluna adicionada: {table_name}.{column_name}')
    return True


def seed_setores(connection):
    for nome in SETORES_PADRAO:
        result = connection.execute(
            text(
                """
                INSERT INTO `setor` (`nome`)
                SELECT :nome
                WHERE NOT EXISTS (
                    SELECT 1 FROM `setor` WHERE `nome` = :nome
                )
                """
            ),
            {'nome': nome}
        )

        if result.rowcount:
            print(f'Setor adicionado: {nome}')


def migrate_atendente(connection, inspector):
    columns = column_names(inspector, 'atividade')
    if 'atendente_id' not in columns:
        add_column_if_missing(connection, inspector, 'atividade', 'atendente_id', 'INT NULL')

    columns = column_names(inspector, 'atividade')
    if 'atendente' in columns:
        connection.execute(text(
            """
            UPDATE `atividade` AS a
            LEFT JOIN `user` AS u
                ON u.`username` = TRIM(a.`atendente`)
                OR (
                    TRIM(a.`atendente`) REGEXP '^[0-9]+$'
                    AND u.`id` = CAST(TRIM(a.`atendente`) AS UNSIGNED)
                )
            SET a.`atendente_id` = u.`id`
            WHERE a.`atendente` IS NOT NULL
              AND TRIM(a.`atendente`) <> ''
              AND a.`atendente_id` IS NULL
            """
        ))

        if LEGACY_ATENDENTE_BACKUP not in columns:
            connection.execute(text(
                f'ALTER TABLE `atividade` CHANGE COLUMN `atendente` `{LEGACY_ATENDENTE_BACKUP}` TEXT NULL'
            ))
            print('Coluna antiga atendente preservada como atendente_legacy.')
        else:
            connection.execute(text('ALTER TABLE `atividade` DROP COLUMN `atendente`'))

    inspector.clear_cache()


def add_atendente_foreign_key(connection, inspector):
    foreign_keys = inspector.get_foreign_keys('atividade')
    already_exists = any(
        fk.get('referred_table') == 'user'
        and fk.get('constrained_columns') == ['atendente_id']
        for fk in foreign_keys
    )
    if already_exists:
        return

    connection.execute(text(
        """
        ALTER TABLE `atividade`
        ADD CONSTRAINT `fk_atividade_atendente`
        FOREIGN KEY (`atendente_id`) REFERENCES `user` (`id`)
        ON DELETE SET NULL
        """
    ))
    print('Chave estrangeira adicionada: atividade.atendente_id -> user.id')


def run_migration():
    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)

        if 'user' not in inspector.get_table_names() or 'atividade' not in inspector.get_table_names():
            raise RuntimeError('As tabelas obrigatórias user e atividade não foram criadas.')

        with db.engine.begin() as connection:
            inspector = inspect(connection)
            seed_setores(connection)
            add_column_if_missing(connection, inspector, 'atividade', 'solicitante', 'VARCHAR(100) NULL')
            add_column_if_missing(connection, inspector, 'atividade', 'atendente_id', 'INT NULL')
            migrate_atendente(connection, inspector)
            add_atendente_foreign_key(connection, inspector)

        print('Migração concluída com sucesso.')


if __name__ == '__main__':
    try:
        run_migration()
    except Exception as error:
        print(f'Erro durante a migração: {error}', file=sys.stderr)
        sys.exit(1)
