from typing import Dict, List, Tuple

import psycopg2

from database.queries import *


class MyPSQLDatabase:

    def __init__(
        self,
        dsn: str
    ) -> None:
        self.dsn = dsn
        self.conn = self.connect(
            dsn=self.dsn
        )

    @staticmethod
    def connect(
        dsn: str
    ):
        keepalive_kwargs = {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 5,
            "keepalives_count": 5,
        }
        return psycopg2.connect(
            dsn=dsn,
            **keepalive_kwargs
        )

    # all tables

    def create_all_tables(
        self
    ) -> None:
        self._execute_and_commit(
            query=create_expert_table_query,
            params=dict()
        )
        self._execute_and_commit(
            query=create_client_table_query,
            params=dict()
        )

    def get_public_schema_tables(
        self
    ) -> List[Tuple]:
        return self._execute_and_fetchall(
            query=select_public_schema_tables_query,
            params=dict()
        )

    def clear_table(
        self,
        table_name: str
    ) -> None:
        return self._execute_and_commit(
            query=delete_from_table_query.format(table_name),
            params=dict()
        )

    # client

    def add_client(
        self,
        tg_user_id: str,
        conversation_state: str = "undefined"
    ) -> None:
        self._execute_and_commit(
            query=insert_client_query,
            params={
                "tg_user_id": tg_user_id,
                "conversation_state": conversation_state
            }
        )

    def get_all_clients(
        self
    ) -> List[Tuple]:
        return self._execute_and_fetchall(
            query=select_all_clients_query,
            params=dict()
        )

    def get_client(
        self,
        tg_user_id: str
    ) -> List[Tuple]:
        return self._execute_and_fetchall(
            query=select_single_client_query,
            params={
                'tg_user_id': tg_user_id
            }
        )

    def update_client(
        self,
        tg_user_id: str,
        conversation_state: str
    ) -> None:
        self._execute_and_commit(
            query=update_client_query,
            params={
                'tg_user_id': tg_user_id,
                'conversation_state': conversation_state
            }
        )

    # expert
    def add_expert(
        self,
        tg_user_id: str
    ) -> None:
        self._execute_and_commit(
            query=insert_expert_query,
            params={
                "tg_user_id": tg_user_id
            }
        )

    def get_all_experts(
        self
    ) -> List[Tuple]:
        return self._execute_and_fetchall(
            query=select_all_experts_query,
            params=dict()
        )

    def get_expert(
        self,
        tg_user_id: str
    ) -> List[Tuple]:
        return self._execute_and_fetchall(
            query=select_single_expert_query,
            params={
                'tg_user_id': tg_user_id
            }
        )

    # utilities

    def _reconnect_if_necessary(
        self
    ) -> None:
        try:
            _ = self.conn.isolation_level
            with self.conn.cursor() as cur:
                cur.execute("SELECT VERSION();")
        except psycopg2.errors.InFailedSqlTransaction as error:
            cur.execute("rollback")
        except (psycopg2.InterfaceError, psycopg2.OperationalError) as error:
            self.conn = self.connect(
                dsn=self.dsn
            )

    def _execute_and_commit(
        self,
        query: str,
        params: Dict
    ) -> None:
        self._reconnect_if_necessary()
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            self.conn.commit()

    def _execute_and_fetchall(
        self,
        query: str,
        params: Dict
    ) -> List[Tuple]:
        self._reconnect_if_necessary()
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
