from datetime import date

from fastapi import FastAPI, Depends

from crud.crud_statistic import *

app = FastAPI()

class DatetimeFilter:
    def init(
            self,
            start_date: date,
            end_date: date
    ):
        self.start_date = start_date
        self.end_date = end_date

@app.get('/statistic/')
async def count_link(filters: DatetimeFilter = Depends()):
    print(filters)
    import pdb
    pdb.set_trace()
    users = await get_links_click_by_date(
        date_from = filters.start_date,
        date_to = filters.end_date

    )
    return users


@app.post("/create-link")
async def create_lin(link: str, click_cost: int):
    users = await create_link(
        link=link,
        click_cost=click_cost
    )
    return users


@app.post("/reset")
async def view_link(link: str):
    users = await reset_statistic(
        link=link
    )
    return users


@app.post("/create-view")
async def view_link(link: str):
    users = await create_view(
        link=link
    )
    return users


@app.post("/create-click")
async def view_link(link: str):
    users = await create_click(
        link=link
    )
    return users


@app.post("/clear-statistics")
async def view_link():
    users = await delete_statistics()
    return users


