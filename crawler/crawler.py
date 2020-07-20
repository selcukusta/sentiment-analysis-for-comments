
from collections import OrderedDict
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def create_random_headers():
    software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                         OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(
        software_names=software_names, operating_systems=operating_systems, limit=100)
    agent = user_agent_rotator.get_random_user_agent()
    headers = {
        "User-Agent": user_agent_rotator.get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Origin": "https://www.trendyol.com",
        "Pragma": "no-cache",
        "Referer": "https://www.trendyol.com/",
        "Sec-Fetch-Dest": "emtpy",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Upgrade-Insecure-Requests": "1"
    }
    return {k: v for k, v in sorted(headers.items(), key=lambda item: item[0])}


if __name__ == "__main__":
    print(create_random_headers())
