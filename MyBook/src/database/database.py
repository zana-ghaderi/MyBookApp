import psycopg2

from psycopg2 import sql

from Intuit.MyBook.src.config.config import POSTGRES_CONFIG

conn = psycopg2.connect(**POSTGRES_CONFIG)


def create_table():
    with conn.cursor() as cur:
        cur.execute("""
                            create table if not exists users
                            id serial primary key,
                            name varchar(255),
                            email varchar(255) unique not null,
                            password_hash varchar(255),
                            role varchar(255)                    
                             """)

        cur.execute("""
                            create table if not exists sales
                            id serial primary key,
                            name varchar(255),
                            email varchar(255) unique not null,
                            password_hash varchar(255),
                            role varchar(255)                    
                             """)

        cur.execute("""
                            create table if not exists invoice
                            id serial primary key,
                            name varchar(255),
                            email varchar(255) unique not null,
                            password_hash varchar(255),
                            role varchar(255)                    
                             """)


create_table()

def insert_record(table, columns, values, conn):
    with conn.cursor() as cur:
        query = sql.SQL("""
        insert into {table} ({columns})
        values ({values})
        returning id;
        """).format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql(sql.Identifier, columns))),
            values=sql.SQL(', ').join(sql.Placeholder*len(values))
        )
        cur.execute(query,values)
        new_id = cur.fetchone()[0]
        return new_id

