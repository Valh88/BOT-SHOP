import json
from aiohttp import ClientSession
from tgbot.config import config


headers = {
   "Accept": "application/json",
   "Rocket-Pay-Key": config.rocket_pay_test,
}

if config.debug:
    url = 'https://dev-pay.ton-rocket.com'
else:
    url = 'https://pay.ton-rocket.com/'


async def get_available_currencies(session: ClientSession,
                                   url: str = url,):

    """ Доступные валюты """
    url = f'{url}/currencies/available'
    res = await session.get(url, headers=headers)
    return await res.json()


async def create_invoice_tg(
        session: ClientSession,
        amount: float,
        currency: str,
        description: str = 'n items',
        hidden_message: str = "thank you",
        callback_url: str = None,
        url: str = url
        # expired_in: int = 86200,
):

    """ Одноразовая платежка """

    # url = 'https://pay.ton-rocket.com/tg-invoices'
    url = f'{url}/tg-invoices'
    data = {
        'amount': amount,
        'currency': currency,
        'description': description,
        'hiddenMessage': hidden_message,
        'callbackUrl': callback_url,
        # 'expiredIn': expired_in,
    }
    res = await session.post(url=url, data=data, headers=headers)
    return await res.json()


async def get_all_currencies(session: ClientSession):
    url = 'https://dev-pay.ton-rocket.com/currencies/available'
    res = await session.get(url=url, headers=headers)
    return await res.json()
