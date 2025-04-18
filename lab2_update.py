import asyncio
import asyncpg

import mimesis
import random


async def update_contracts(conn):
    gen = mimesis.Generic()
    start = gen.datetime.date()
    end = gen.datetime.date()
    diff = end - start
    if diff.days < 0:
        start, end = end, start
        diff = end - start
    await conn.execute('UPDATE contracts SET duration=$1 WHERE "PK_contract"=$2', diff, 3)


async def update_companies(conn):
    await conn.execute('UPDATE companies SET company=$1 WHERE company=$2', 'ПАО мегафон', 'ПАО ростелеком')


async def update_parking(conn):
    await conn.execute('UPDATE parking SET "FK_company"=$1 WHERE "FK_company"=$2', 2, 1)


async def update_floors(conn):
    await conn.execute('UPDATE floors SET floor=$1 WHERE floor=$2', 'B1', 'A5')


async def update_offices(conn):
    await conn.execute('UPDATE offices SET area=$1 WHERE office=$2', random.randint(100, 400), 'A4')


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
        update_contracts(conn), update_companies(conn),
        update_parking(conn), update_floors(conn),
        update_offices(conn)
    ]

    for task in tasks:
        await asyncio.create_task(task)


asyncio.run(main())