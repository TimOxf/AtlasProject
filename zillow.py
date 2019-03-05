import requests
from xml.etree import ElementTree as ET


def getZillow(address, citystatezip):
    """
    Takes address and citystatezip and returns a list with link to listing and status (for rent or not)
    """
    zws_id = "xxxxxxxxxx"
    url = "https://www.zillow.com/webservice/GetSearchResults.htm"

    querystring = {
        "zws-id": zws_id,
        "address": address,
        "citystatezip": citystatezip
    }

    response = requests.request(
        "GET", url, params=querystring)


    parsed_response = ET.fromstring(response.text)


    zpid = parsed_response.find('response/results/result/zpid')

    #check if zpid was found and return "status unavailable if so"
    if zpid==None:
        return ["","Status Unavailable"]


    zpid = zpid.text
    link = parsed_response.find(
    'response/results/result/links/homedetails').text


    # Get the status of the property
    url2 = "http://zm.zillow.com/web-services/HomeDetails"

    querystring2 = {"zws-id": zws_id,
                   "zpid": zpid,
                   "jsonver": "0"}

    headers = {
                        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    					'accept-encoding':'gzip, deflate, sdch, br',
    					'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
    					'cache-control':'max-age=0',
    					'upgrade-insecure-requests':'1',
    					'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    response2 = requests.request(
        "GET", url2, params=querystring2, headers=headers)

    status = response2.json()["homeSummary"]["displayType"]
    #print(response2)

    return [link, status]
