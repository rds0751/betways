from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistories, Withdrawals, Paymentoptions
from binary.models import BinaryTree
from zone.models import ZoneUpgrades
import requests
import jwt
from django.utils import timezone

class Command(BaseCommand):
    help = "Update Binary Data"
    def handle(self, *args, **options):
        time = timezone.now()
        secret = '1451-600d130516c8f-989033'
        email = 'balistarkumar091297@gmail.com'
        url = "https://services.apiscript.in/jwt_encode"
        username = "APIHA10337901"
        password = "Smarty@248"

        payload = "secret_key={}&email_id={}".format(secret, email)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'postman-token': "397273e7-d3b6-416d-c7ce-ffeb722adaf9"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        data = response.json()
        encode_token = data['encode_token']
        print(encode_token)
        print(jwt.decode(encode_token, secret, algorithms=['HS256']))

        # Transaction
        url = "https://services.apiscript.in/dmt/express_fund_transfer"

        payload = "username={}&pwd={}&account_no=50200030683011&ifsc=HDFC0000191&upi_id=rds0751%40paytm&amount=51&transfer_mode=IMPS&client_id=145470435&token={}".format(username, password, encode_token)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'authorization': "Digest username=\"\", realm=\"\", nonce=\"\", uri=\"/dmt/express_fund_transfer\", response=\"3e73127784fc3e52ccf0b55e91c87c4b\", opaque=\"\"",
            'cache-control': "no-cache",
            'postman-token': "2d2d3007-a70b-2dda-e781-c47221c45df9"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)