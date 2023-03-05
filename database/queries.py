# all tables

create_expert_table_query = """
CREATE TABLE
IF NOT EXISTS
Expert (
    "expert_id" serial PRIMARY KEY,
    "tg_user_id" varchar(18) NOT NULL
)
;
"""

create_client_table_query = """
CREATE TABLE
IF NOT EXISTS
Client (
    "client_id" serial PRIMARY KEY,
    "tg_user_id" varchar(18) NOT NULL,
    "conversation_state" varchar(50) NOT NULL DEFAULT 'undefined'
)
;
"""

select_public_schema_tables_query = """
SELECT
    table_name
FROM
    information_schema.tables
WHERE
    table_schema = 'public'
;
"""

delete_from_table_query = """
DELETE FROM
    {0}
;
"""

# client-related queries

insert_client_query = """
INSERT INTO Client
    (tg_user_id, conversation_state)
VALUES
    (%(tg_user_id)s, %(conversation_state)s)
;
"""

select_all_clients_query = """
SELECT
    *
FROM
    Client
;
"""

select_single_client_query = """
SELECT
    *
FROM
    Client
WHERE
    tg_user_id = %(tg_user_id)s
;
"""

update_client_query = """
UPDATE
    Client
SET
    conversation_state = %(conversation_state)s
WHERE
    tg_user_id = %(tg_user_id)s
;
"""

# expert-related queries

insert_expert_query = """
INSERT INTO Expert
    (tg_user_id)
VALUES
    (%(tg_user_id)s)
;
"""

select_all_experts_query = """
SELECT
    *
FROM
    Expert
;
"""

select_single_expert_query = """
SELECT
    *
FROM
    Expert
WHERE
    tg_user_id = %(tg_user_id)s
;
"""
