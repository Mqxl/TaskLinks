import asyncio
import datetime

import models
from alembic.devsettings import session
from sqlalchemy import select, func, insert,delete

async def get_avg_cost_price(
    link:str,
):
    stmt = select(
        models.Links.click_cost
    ).where(
        models.Links
    ).join(models.Links, models.Links.link == link)
    record1 = (await session.execute(stmt)).one()

    second_stmt = select(
        func.count(models.Clicks.id)
    ).where(
        models.Clicks.link_id == models.Links.id
    ).join(models.Clicks, models.Links.link == link)
    record2 = (await session.execute(second_stmt)).one()
    return record1/record2

async def get_avg_cost_views(
    link: str,
):
    stmt = select(
        models.Views
    ).where(
        models.Views.link_id == models.Links.id
    ).join(models.Links, models.Links.link == link)
    record1 = (await session.execute(stmt)).one()
    return record1/1000

async def get_links_click_by_date(
    link: str,
    date_from: datetime.datetime,
    date_to: datetime.datetime,
):
    stmt = select(
        models.Links.id
    ).where(
        models.Links.link == link
    )
    record = (await session.execute(stmt)).one()
    second_stmt = select(
        func.count(models.Clicks.id)
    ).where(
        models.Clicks.link_id == record,
        models.Clicks.date <= date_from,
        models.Clicks.date >= date_to
    )
    record = (await session.execute(second_stmt)).one()
    return record

async def reset_statistic(
        link: str,
):
    cte = select(models.Links.id).where(models.Links.link == link).cte("link")
    delete_stmt1 = delete(models.Views).where(models.Views.link_id == cte.c.id)
    await asyncio.gather(session.execute(delete_stmt1), session.execute(delete_stmt1))
    await session.commit()
    return
    
async def create_view(
        link: str
):
    stmt = select(models.Links)
    record = (await session.execute(stmt)).all()
    return record


async def create_click(
        link: str
):
    stmt = select(models.Links)
    record = (await session.execute(stmt)).all()
    return record


async def create_link(
        link: str,
        cost_price: int
):
    stmt = insert(models.Links).values(link=link, click_cost=cost_price)
    await session.execute(stmt)
    await session.commit()
    return

async def delete_table():
   stmt=delete(models.links).where(models.Links.id==1)
   await session.execute(stmt).one()
   await session.commit()



