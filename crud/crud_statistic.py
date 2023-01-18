import asyncio

from datetime import datetime
import models
from alembic.devsettings import session
from sqlalchemy import select, func, insert, delete, and_,or_


async def get_avg_cost_price(
        link: str,
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
    return record1 / record2


async def get_avg_cost_views(
        link: str,
):
    stmt = select(
        models.Views
    ).where(
        models.Views.link_id == models.Links.id
    ).join(models.Links, models.Links.link == link)
    record1 = (await session.execute(stmt)).one()
    return record1 / 1000


async def get_links_click_by_date(
        date_from: datetime.date,
        date_to: datetime.date,
):

    date_from = datetime.combine(date_from, datetime.max.time())
    date_to = datetime.combine(date_to,datetime.max.time())
    stmt = select(models.Links, models.Clicks, models.Views).where(or_(and_(models.Clicks.date <= date_from,models.Clicks.date >= date_to),and_(models.Views.date <= date_from,models.Views.date >= date_to)))
    record = (await session.execute(stmt)).all()
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
    cte = select(models.Links).where(models.Links.link == link).cte("link")
    stmt = insert(models.Views).values(link_id=cte.c.id)
    record = (await session.execute(stmt)).all()
    await session.commit()
    return record


async def create_link(
        link: str,
        click_cost: int
):
    """
    Working
    """
    stmt = insert(models.Links).values(link=link, click_cost=click_cost).returning(models.Links)
    record = (await session.execute(stmt)).all()
    await session.commit()
    return record




async def delete_statistics():
    stmt = delete(models.Views)
    stmt2 = delete(models.Views)
    await asyncio.gather(session.execute(stmt), session.execute(stmt2))
    await session.commit()
