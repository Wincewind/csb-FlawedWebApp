import requests

def test_bac(sessionid, csrf):
	address = 'http://127.0.0.1:8000/secret/1'
	cookies = {'sessionid':sessionid,'csrftoken':csrf}
	payload = {'new_secret':"You´ve been hacked!'; --"}
	response = requests.post(url=address,data=payload,timeout=1,cookies=cookies)
	return response


if __name__ == '__main__':
    sessionid = input('Input here a active sessionid: ')
    csrf = input('Input here a active csrftoken: ')
    print(test_bac(sessionid,csrf))
