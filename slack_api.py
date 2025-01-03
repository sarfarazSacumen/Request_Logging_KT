"""Slack API call"""

import requests
from requests.adapters import HTTPAdapter
import logging
import json

class Slack:
    def __init__(self, base_url, access_token):
        """Initializing base url, headers with bearer token, and configuring the logger

        Args:
            base_url : Slack API base url
            access_token : Slack bot token
        """
        self.base_url = base_url
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel("DEBUG")

        console_handler = logging.StreamHandler()
        console_handler.setLevel("DEBUG")
        file_handler = logging.FileHandler("slackLog.log", mode="w", encoding="utf-8")
        file_handler.setLevel(10)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        console_formatter = logging.Formatter("%(levelname)s-%(name)s-%(message)s")
        file_formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(name)s-%(message)s")

        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

    def get_converetsion_list(self):
        """List out all the channel names
        """
        slack_adapter = HTTPAdapter(max_retries=2)
        session = requests.Session()

        try:
            session.mount(f"{self.base_url}/conversations.list", slack_adapter)
            response = session.get(f"{self.base_url}/conversations.list", headers = self.headers, timeout = 3)
        except Exception as e:
            self.logger.exception(f"{e}")
        
        self.logger.debug(f"URL = {response.url}")
        self.logger.debug(f"Status code = {response.status_code}")

        try:
            json_data = response.json()
            json_pretty = json.dumps(json_data, indent=4)
            self.logger.info(f"JSON Data = {json_pretty}")
        except Exception as e:
            self.logger.exception(f"Content Not Found {e}")

    def get_user_list(self):
        """List out all user details
        """
        slack_adapter = HTTPAdapter(max_retries=2)
        session = requests.Session()

        try:
            session.mount(f"{self.base_url}/users.list", slack_adapter)
            response = session.get(f"{self.base_url}/users.list", headers = self.headers, timeout = 3)
        except Exception as e:
            self.logger.exception(f"{e}")
        
        self.logger.debug(f"URL = {response.url}")
        self.logger.debug(f"Status code = {response.status_code}")

        try:
            json_data = response.json()
            json_pretty = json.dumps(json_data, indent=4)
            self.logger.info(f"JSON Data = {json_pretty}")
        except Exception as e:
            self.logger.error(f"Content Not Found {e}", exc_info=True)

base_url = "https://slack.com/api"
access_token = "xoxb-8228632731095-8243326122850-mcjoXx2EreYxd678slNavcZJ"

slack = Slack(base_url, access_token)
slack.get_converetsion_list()
slack.get_user_list()