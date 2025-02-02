import json
import logging
from typing import List, Dict
import socket


STANDARD_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=STANDARD_FORMAT)
Error_log = logging.getLogger("Error_log")
Error_log.setLevel(logging.ERROR)
the_stream_handler = logging.StreamHandler()
the_file_handler = logging.FileHandler("error.log")
the_stream_handler.setFormatter(logging.Formatter(STANDARD_FORMAT))
the_file_handler.setFormatter(logging.Formatter(STANDARD_FORMAT))
Error_log.addHandler(the_stream_handler)
Error_log.addHandler(the_file_handler)
Info_log = logging.getLogger("Info_log")
Info_log.setLevel(logging.INFO)
Info_log.addHandler(the_stream_handler)
Info_log.addHandler(the_file_handler)


def fetch_dns() -> List[Dict[str, str]]:
    """ Fetching DNS's from a json file """
    default_dns = [
                {"primary": "8.8.8.8", "secondary": "8.8.4.4"},
                {"primary": "1.1.1.1", "secondary": "1.0.0.1"},
                {"primary": "208.67.222.222", "secondary": "208.67.220.220"},
                {"primary": "9.9.9.9", "secondary": "149.112.112.112"},
                {"primary": "8.26.56.26", "secondary": "8.20.247.20"},
                {"primary": "45.90.28.0", "secondary": "45.90.30.0"},
                {"primary": "77.88.8.8", "secondary": "77.88.8.1"},
                {"primary": "185.228.168.9", "secondary": "185.228.169.9"}
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


def check_for_wifi() -> bool:
    """
    Check if the device has an internet connection via DNS check's
    """
    # the best way to check if there is an internet connection in the internet
    retry = 3
    backoff = 1
    for i in range(retry):
        for i in fetch_dns():
            try:
                Info_log.info("Trying to connect to %s", i["primary"])
                with socket.create_connection((i["primary"], 53)):
                    return True
            except (socket.gaierror, socket.timeout):
                continue
            except OSError:
                try:
                    Info_log.info("Trying to connect to %s", i["secondary"])
                    with socket.create_connection((i["secondary"], 53)):
                        return True
                except (socket.gaierror, socket.timeout):
                    continue
                except OSError:
                    continue
        backoff *= 2
    return False
