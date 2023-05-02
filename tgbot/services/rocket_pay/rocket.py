import json
from aiohttp import ClientSession
from tgbot.config import config


_headers = {
   "Accept": "application/json",
   "Rocket-Pay-Key": config.rocket_pay_test,
}

_session = ClientSession(headers=_headers)

if config.debug:
    _url = 'https://dev-pay.ton-rocket.com/'
else:
    _url = 'https://pay.ton-rocket.com/'


async def get_available_currencies(request):

    """ Доступные валюты """
    url = f'{_url}currencies/available'
    res = await request.get(url=url)
    return await res.json()


async def create_invoice_tg(
        amount: float,
        currency: str,
        description: str = 'n items',
        hidden_message: str = "thank you",
        callback_url: str = None,
        expired_in: int = 86200,
):

    """ Одноразовая платежка """

    # url = 'https://pay.ton-rocket.com/tg-invoices'
    url = f'{_url}tg-invoices'
    data = {
        'amount': amount,
        'currency': currency,
        'description': description,
        'hiddenMessage': hidden_message,
        'callbackUrl': callback_url,
        'expiredIn': expired_in,
    }
    async with ClientSession(headers=_headers) as request:
        res = await request.post(url=url, json=data)
    return await res.json()


async def get_all_currencies():
    url = f'{_url}currencies/available'
    async with ClientSession(headers=_headers) as request:
        res = await request.get(url=url)
    return await res.json()
