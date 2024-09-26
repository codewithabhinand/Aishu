import requests as rq


def main():
    try:
        res = rq.get("https://weatherapihere.com/api/get-endpoint")
        res = res.json()
    except Exception as e:
        res = {"temprature":"No Data"}
    return res