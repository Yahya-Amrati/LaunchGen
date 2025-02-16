
import json
import logging
from typing import List, Dict
import socket

# Cette partie à été coder entierement par Yahya Amrati
# -> 02/02/2025

STANDARD_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=STANDARD_FORMAT)
Error_log = logging.getLogger("Error_log")
Error_log.setLevel(logging.ERROR)
the_stream_handler = logging.StreamHandler()
the_file_handler = logging.FileHandler("logs.log")
the_file_handler.setFormatter(logging.Formatter(STANDARD_FORMAT))
Error_log.addHandler(the_file_handler)
Info_log = logging.getLogger("Info_log")
Info_log.setLevel(logging.INFO)
Info_log.addHandler(the_file_handler)


def fetch_dns() -> List[Dict[str, str]]:
    """Fetching DNS's from a json file"""
    default_dns = [
        {"primary": "8.8.8.8", "secondary": "8.8.4.4"},
        {"primary": "1.1.1.1", "secondary": "1.0.0.1"},
        {"primary": "208.67.222.222", "secondary": "208.67.220.220"},
        {"primary": "9.9.9.9", "secondary": "149.112.112.112"},
        {"primary": "8.26.56.26", "secondary": "8.20.247.20"},
        {"primary": "45.90.28.0", "secondary": "45.90.30.0"},
        {"primary": "77.88.8.8", "secondary": "77.88.8.1"},
        {"primary": "185.228.168.9", "secondary": "185.228.169.9"},
    ]
    try:
        with open("dns.json", "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            data = data["dns"]
            return data
    except json.JSONDecodeError:
        Error_log.error("dns.json is not a valid json file")
        return default_dns
    except FileNotFoundError:
        Error_log.error("dns.json not found")
        with open("dns.json", "w", encoding="utf-8") as f:
            json.dump({"dns": default_dns}, f)
            return default_dns
    except PermissionError:
        Error_log.error("dns.json is not accessible due to lack of permission")
        return default_dns
    except UnicodeTranslateError:
        Error_log.error("dns.json is has not a valid encoding type")
        return default_dns


def check_for_internet() -> bool:
    """
    Check if the device has an internet connection via DNS check's
    """
    # the best way to check if there is an internet connection in the internet
    retry = 3
    backoff = 1
    for _ in range(retry):
        for b in fetch_dns():
            Info_log.info("Trying to connect to DNS %s", b["primary"])
            try:
                with socket.create_connection((b["primary"], 53)):
                    return True
            except (socket.gaierror, socket.timeout):
                continue
            except OSError:
                Info_log.info("Trying to connect to DNS %s", b["secondary"])
                try:
                    with socket.create_connection((b["secondary"], 53)):
                        return True
                except (socket.gaierror, socket.timeout):
                    continue
                except OSError:
                    continue
        backoff *= 2
    Error_log.error("Failed to connect to any DNS")
    return False
