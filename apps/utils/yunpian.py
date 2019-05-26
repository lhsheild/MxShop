import requests

from MxShop.settings import APIKEY


class YunPian():
    def __init__(self, api_key=APIKEY):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            "api_key":self.api_key,
            "mobile": mobile,
            "text": "您的验证码是{code}".format(code=code)
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = response.json()
        print(re_dict)
        return re_dict


if __name__ == '__main__':
    yunpian = YunPian('test')
    yunpian.send_sms(2019, 13737577320)