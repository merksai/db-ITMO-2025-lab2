import asyncio
import asyncpg

import mimesis
import random


async def delete_contracts(conn):
    await conn.execute('DELETE FROM contracts WHERE "PK_contract"=$1', 4)


async def delete_passes(conn):
    await conn.execute('DELETE FROM passes WHERE "PK_pass"=$1', 9)


async def delete_parking(conn):
    await conn.execute('DELETE FROM parking WHERE "PK_parking"=$1', 2)
    await conn.execute('DELETE FROM parking WHERE "PK_parking"=$1', 3)


async def delete_offices(conn):
    await conn.execute('DELETE FROM offices WHERE office=$1', 'A5')


async def main():
    conn = await asyncpg.connect(
        user='...',
        password='...',
        database='business_center',
        host='localhost',
        port='5432'
    )
    await conn.execute('SET search_path TO main')

    tasks = [
        delete_contracts(conn), delete_passes(conn),
        delete_parking(conn), delete_offices(conn)
    ]

    for task in tasks:
        await asyncio.create_task(task)


asyncio.run(main())