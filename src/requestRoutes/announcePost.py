import requests

def announceClient(config):
    announcement = requests.post(config['SERVER']['url'] + '/v1/announce')

    return announcement.json()

