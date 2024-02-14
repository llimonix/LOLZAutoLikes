import time
from src.client import LZT
from src.env import load_config
import asyncio
import logging


async def login(lzt, config):
    await lzt.login({
        'xf_user': config.XF_USER,
        'xf_tfa_trust': config.XF_TFA_TRUST,
    })
    return lzt


async def main(lzt, latest, u):
    try:
        posts = await lzt.fetch_new_posts()
        for item in posts:
            if item.id == latest or item.liked:
                break

            skip_user = item.author_group in [2, 21, None]
            cooldown = time.time() - u.get(item.author, 0) < 30 * 60
            if skip_user or cooldown:
                continue

            u[item.author] = time.time()
            await lzt.like(item.id)
            logging.info(f"Поставил лайк {item.author} на сообщение с ID: {item.id}")
            await asyncio.sleep(5)

        if posts:
            latest = posts[0].id

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

    await asyncio.sleep(15)
    return latest


if __name__ == "__main__":
    config = load_config(".env")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    async def main_async():
        lzt = LZT()
        await login(lzt, config)

        latest = 0
        u = {}

        while True:
            latest = await main(lzt, latest, u)


    asyncio.run(main_async())
