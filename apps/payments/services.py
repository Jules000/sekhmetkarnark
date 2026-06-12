import json
import logging
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)


class TranzakError(Exception):
    pass


class TranzakClient:
    def __init__(self):
        self.app_id = settings.TRANZAK_APP_ID
        self.app_key = settings.TRANZAK_APP_KEY
        self.base_url = settings.TRANZAK_API_BASE_URL
        self._access_token = None

    def _get_access_token(self):
        url = urljoin(self.base_url, "oauth/token")
        try:
            resp = requests.post(
                url,
                json={"grant_type": "client_credentials"},
                auth=(self.app_id, self.app_key),
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            self._access_token = data["access_token"]
            return self._access_token
        except requests.RequestException as e:
            logger.error("Tranzak auth failed: %s", e)
            raise TranzakError(f"Authentication failed: {e}")

    def _headers(self):
        if not self._access_token:
            self._get_access_token()
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

    def create_checkout(self, amount, currency, reference, success_url, cancel_url, description=""):
        url = urljoin(self.base_url, "payment/checkout")
        payload = {
            "amount": str(amount),
            "currency": currency,
            "reference": reference,
            "successUrl": success_url,
            "cancelUrl": cancel_url,
            "description": description,
        }
        try:
            resp = requests.post(
                url,
                json=payload,
                headers=self._headers(),
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.error("Tranzak checkout failed: %s", e)
            raise TranzakError(f"Checkout creation failed: {e}")

    def get_transaction_status(self, transaction_id):
        url = urljoin(self.base_url, f"payment/transaction/{transaction_id}")
        try:
            resp = requests.get(
                url,
                headers=self._headers(),
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.error("Tranzak status check failed: %s", e)
            raise TranzakError(f"Status check failed: {e}")
