from requests import get
import urllib.request
from ipaddress import ip_address


def check_internet_connection():
    try:
        urllib.request.urlopen("https://www.google.com")
        return True
    except urllib.error.URLError:
        return False


def get_public_ip():
    if check_internet_connection():
        return get("https://api64.ipify.org").text
    else:
        return "[Error:1]"


def is_ipv4(ip):
    if ip_address(ip).version == 4:
        return True
    else:
        return False


def is_ipv6(ip):
    if ip_address(ip).version == 6:
        return True
    else:
        return False
