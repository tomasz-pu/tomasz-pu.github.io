import requests

def share(link, descr, img, email="blank"):
    url = 'https://automex.pupel.xyz/api/kodi/share'
    #url = 'http://localhost/automex/public/api/kodi/share'
    payload = {"url": link, "descr": descr, "img": img, "email": email}
    requests.post(url, data=payload, verify=False)

def get_shared(page_no, limit):
    url = 'https://automex.pupel.xyz/api/kodi/get-shared'
    #url = 'http://localhost/automex/public/api/kodi/get-shared'

    payload = {"page_no": page_no, "limit": limit}

    _r = requests.post(url, data=payload, verify=False)

    return _r.text

def ping(data_dict):
    _url = 'https://hc-ping.com'
    _monitor_id = '4109355c-2f6f-413b-9127-addbadfe5793'
    data_string = "&".join(["=".join([str(x[0]),str(x[1])]) for x in data_dict.items()])
    requests.post(f"{_url}/{_monitor_id}", data=data_string)