import asyncio
import asyncpg

import mimesis
import random


async def init_contracts(conn):
    data = []

    gen = mimesis.Generic()
    for i in range(1, 6):
        signed_date = gen.datetime.date(start=2015, end=2025)
        start = gen.datetime.date()
        end = gen.datetime.date()
        diff = end - start
        if diff.days < 0:
            start, end = end, start
            diff = end - start
        data.append((i, signed_date, diff))

    await conn.executemany('INSERT INTO contracts VALUES ($1, $2, $3)', data)


async def init_positions(conn):
    positions = [(1, 'manager'), (2, 'security'), (3, 'cleaner'), (4, 'repairman')]
    await conn.executemany('INSERT INTO positions VALUES ($1, $2)', positions)


async def init_passes(conn):
    data = []

    gen = mimesis.Generic()
    for i in range(1, 11):
        receipt_date = gen.datetime.date(start=2015, end=2025)
        start = gen.datetime.date()
        end = gen.datetime.date()
        diff = end - start
        if diff.days < 0:
            start, end = end, start
            diff = end - start
        data.append((i, receipt_date, diff))

    await conn.executemany('INSERT INTO passes VALUES ($1, $2, $3)', data)


async def init_companies(conn):
    data = []
    companies = ['ООО рога и копыта', 'ПАО ростелеком', 'АО русское лото', 'ООО контора', 'ИП БЛИНОВСКАЯ']
    FKs_constract = [1, 2, 3, 4, 5]
    random.shuffle(FKs_constract)

    gen = mimesis.Generic()
    for i in range(1, 6):
        start = gen.datetime.time()
        end = gen.datetime.time()
        if start > end:
            start, end = end, start
        data.append((i, companies[i - 1], start, end, FKs_constract[i - 1]))

    await conn.executemany('INSERT INTO companies VALUES ($1, $2, $3, $4, $5)', data)


async def init_parking(conn):
    data = []
    FKs_companies = [1, 2, 3, 4, 5]
    random.shuffle(FKs_companies)
    letters = ['A', 'B', 'C', 'D', 'E']
    numbers = ['11', '3', '7', '12', '34']

    for i in range(1, 6):
        data.append((i, random.choice(letters) + numbers[i - 1], FKs_companies[i - 1]))

    await conn.executemany('INSERT INTO parking VALUES ($1, $2, $3)', data)


async def init_employees(conn):
    data = []
    patronymics = ['Александрович', 'Петрович', 'Иванович', 'Сергеевич', 'Михайлович']
    FKs_passes = [i for i in range(1, 11)]
    random.shuffle(FKs_passes)

    gen = mimesis.Generic(locale='ru')
    for i in range(1, 11):
        first_name = gen.person.first_name()
        last_name = gen.person.last_name()
        patronymic = random.choice(patronymics)
        data.append((i, first_name, last_name, patronymic, FKs_passes[i - 1]))

    await conn.executemany('INSERT INTO employees VALUES ($1, $2, $3, $4, $5)', data)


async def init_company_employees(conn):
    data = []
    FKs_employees = [1, 2, 5, 8, 9]
    random.shuffle(FKs_employees)
    FKs_companies = [1, 2, 3, 4, 5]
    random.shuffle(FKs_companies)

    for i in range(1, 6):
        data.append((FKs_employees[i - 1], FKs_companies[i - 1]))

    await conn.executemany('INSERT INTO company_employees VALUES ($1, $2)', data)


async def init_business_center_staff(conn):
    data = []
    FKs_employees = [3, 4, 6, 7, 10]
    random.shuffle(FKs_employees)
    FKs_senior_staff = [3, 7]
    random.shuffle(FKs_senior_staff)
    FKs_positions = [2, 3, 4]
    random.shuffle(FKs_positions)

    for i in range(1, 6):
        if FKs_employees[i - 1] in [3, 7]:
            data.append((FKs_employees[i - 1], None, 1))
        else:
            data.append((FKs_employees[i - 1], FKs_senior_staff[i % 2], FKs_positions[i % 3]))

    await conn.executemany('INSERT INTO business_center_staff VALUES ($1, $2, $3)', data)


async def init_floors(conn):
    data = []
    FKs_senior_staff = [3, 7]
    random.shuffle(FKs_senior_staff)

    for i in range(1, 6):
        data.append((i, f'A{i}', FKs_senior_staff[i % 2]))

    await conn.executemany('INSERT INTO floors VALUES ($1, $2, $3)', data)


async def init_offices(conn):
    data = []
    FKs_companies = [1, 2, 3, 4, 5]
    random.shuffle(FKs_companies)
    FKs_floors = [1, 2, 3, 4, 5]
    random.shuffle(FKs_floors)

    for i in range(1, 6):
        data.append((i, f'A{i}', random.randint(100, 400), FKs_companies[i - 1], FKs_floors[i - 1]))

    await conn.executemany('INSERT INTO offices VALUES ($1, $2, $3, $4, $5)', data)


async def clear_db():
    tables = [
        'contracts', 'positions',
        'passes', 'companies',
        'parking', 'employees',
        'company_employees', 'business_center_staff',
        'floors', 'offices'
    ]

    conn = await asyncpg.connect(
        user='...',
        password='...',
        database='business_center',
        host='localhost',
        port='5432'
    )
    await conn.execute('SET search_path TO main')

    for table in tables:
        await conn.execute(f'TRUNCATE TABLE {table} CASCADE')


async def main():
    conn = await asyncpg.connect(
        user='merksai',
        password='ebuprincess',
        database='business_center',
        host='localhost',
        port='5432'
    )
    await conn.execute('SET search_path TO main')

    tasks = [
        init_contracts(conn), init_positions(conn),
        init_passes(conn), init_companies(conn),
        init_parking(conn), init_employees(conn),
        init_company_employees(conn), init_business_center_staff(conn),
        init_floors(conn), init_offices(conn)
    ]

    for task in tasks:
        await asyncio.create_task(task)


asyncio.run(clear_db())
asyncio.run(main())