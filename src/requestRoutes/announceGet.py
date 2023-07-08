import requests

def getAnnouncedClient(config, id):
    client = requests.get(config['SERVER']['url'] + '/v1/announce', params={'id': id})

    return client.json()