import re
from bs4 import BeautifulSoup
import aiohttp
from urllib.parse import urlencode
from src.cookie_builder import build_cookie
from src.env import load_config
from src.post_parser import parse_post

class LZT:
    def __init__(self):
        self.config = load_config("config.env")
        self.xf_token = ''
        self.headers = {
            'Cookie': '',
            'User-Agent': self.config.USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    async def login(self, cookies):
        self.headers['Cookie'] = build_cookie({
            'dfuid': await self.get_df_uid(),
            'xf_user': cookies['xf_user'],
            'xf_tfa_trust': cookies['xf_tfa_trust']
        })

    async def set_proxy(self):
        proxy_enabled = self.config.PROXY_EXISTS
        if proxy_enabled:
            return f'http://{self.config.PROXY}'
        else:
            return None

    async def get_df_uid(self):
        async with aiohttp.ClientSession(headers={'User-Agent': self.config.USER_AGENT}) as session:
            async with session.get('https://zelenka.guru', proxy=await self.set_proxy()) as response:
                body = await response.text()

        return re.search(r'max\|(\w+)\|navigator', body).group(1)

    async def fetch_new_posts(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://zelenka.guru/find-new/profile-posts', headers=self.headers,
                                   proxy=await self.set_proxy()) as response:
                page = await response.text()

        xf_token_match = re.search(r'name="_xfToken" value="([\w,]+)"', page)

        if not xf_token_match:
            return []
        else:
            self.xf_token = xf_token_match.group(1)

        soup = BeautifulSoup(page, 'html.parser')
        posts = soup.select('.messageSimple')
        return [parse_post(post) for post in posts]

    async def like(self, post_id):
        url = f'https://zelenka.guru/profile-posts/{post_id}/like'
        params = {
            '_xfToken': self.xf_token,
            '_xfResponseType': 'json'
        }
        body = urlencode(params)
        headers = self.headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=body, proxy=await self.set_proxy()):
                pass
