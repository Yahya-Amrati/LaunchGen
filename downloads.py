import json
from typing import Callable, List
import os
import requests
from requests.adapters import HTTPAdapter
import urllib3
import Utils_minecraft
import Utils_net

path: str = os.path.join(Utils_minecraft.local_path(), "LaunchGen")
session = requests.Session()
Retry = urllib3.Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=Retry))
session.mount("http://", HTTPAdapter(max_retries=Retry))

def Error_handler(func) -> Callable:
    """this is a decorator for handling errors"""
    def wrapper(*args, **kwargs) -> Callable | None:
        try:
            if not Utils_net.check_for_internet():
                return Utils_net.Error_log.error("No internet connection")
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError:
            Utils_net.Error_log.error("We had a http error")
        except json.JSONDecodeError:
            Utils_net.Error_log.error("We had a json error")
        except OSError:
            Utils_net.Error_log.error("We had a OSError")
        except Exception as e:
            Utils_net.Error_log.error("Couldn't finish task due to %s", e)
    return wrapper

@Error_handler
def fetch(url: str) -> dict:
    """this is a function for fetching data"""
    response = session.get(url)
    response.raise_for_status()
    return json.loads(response.text)

@Error_handler
def download(data: dict) -> None:
    """this is a function for downloading data"""
    os.makedirs(path, exist_ok=True)
    os.chdir(path)
    url: List[str] = data.get("latest")["urls"]
    for i in url:
        Utils_net.Info_log.info("Downloading %s", i)
        response = session.get(i)
        response.raise_for_status()
        with open(os.path.join(path, data.get("latest")["filename"]), "wb") as f:
            f.write(response.content)

def main() -> None:
    FETCH_URL = "..."
    data = fetch(FETCH_URL)
    download(data)
    Utils_net.Info_log.info("Downloads finished")