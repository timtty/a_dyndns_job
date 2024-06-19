import requests
import socket
import asyncio
import time
import os
from loguru import logger


DNS_HOST = os.environ.get("DNS_HOST", "none")
DNS_DOMAIN = os.environ.get("DNS_DOMAIN", "none")
DNS_PASS = os.environ.get("DNS_PASS", "none")


def update_host(new_ip_address):
    url = "https://dynamicdns.park-your-domain.com/update"
    params = {
        "host": DNS_HOST,
        "domain": DNS_DOMAIN,
        "password": DNS_PASS,
        "ip": new_ip_address
    }

    res = requests.get(url=url, params=params)

    if res.status_code == 200:
        logger.success(f"DYN-DNS executed successfully: {res.content}")
        return True

    else:
        logger.error(f"DYN-DNS API error: {res.content}")
        return False


def get_my_ip():
    res = requests.get("https://api.ipify.org")

    if res.status_code == 200:
        return res.text

    else:
        logger.error(f"Unable to get IP. {res.status_code} - {res.text}")
        return False


def run():
    full_domain = f"{DNS_HOST}.{DNS_DOMAIN}"

    while True:
        last_ip = socket.gethostbyname(full_domain)
        current_ip = get_my_ip()

        if current_ip:
            if last_ip != current_ip:
                logger.warning(f"IP address has changed from {last_ip} to {current_ip}")

                if update_host(current_ip):
                    logger.success(f"Successfully updated IP from {last_ip} to {current_ip}")

        time.sleep(60 * 60)


if __name__ == "__main__":
    run()
