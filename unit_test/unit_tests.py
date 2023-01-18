import unittest
from GeoDataProject.main import *


class TestFactorial(unittest.TestCase):
    async def test_view_link(self):
        link = "https://habr.com/ru/post/97075/"
        users = await get_avg_cost_price(
            link=link
        )
        assert users.link == link

    async def test_view_link(self):
        link="https://habr.com/ru/post/97075/"
        users = await reset_statistic(
            link=link
        )
        assert users.link == link

    async def test_view_link(self):
        link = "https://habr.com/ru/post/97075/"
        users = await create_view(
            link=link
        )
        assert users.link == link

    async def test_view_link(self):
        link = "https://habr.com/ru/post/97075/"
        users = await delete_table(
            link=link
        )
        assert users.link == link

    async def test_view_link(self):
        link = "https://habr.com/ru/post/97075/"
        users = await get_avg_cost_views(
            link=link
        )
        assert users.link == link

    async def test_view_link(self):
        link = "https://habr.com/ru/post/97075/"
        users = await create_click(
            link=link
        )
        assert users.link == link

    async def test_view_link(self):
        link = "https://habr.com/ru/post/97075/"
        date_from = datetime.datetime.now() - datetime.timedelta(hours=1)
        date_to = datetime.datetime.now()
        users = await get_links_click_by_date(
            link=link,
            date_from=date_from,
            date_to=date_to
        )
        assert users.link == link
