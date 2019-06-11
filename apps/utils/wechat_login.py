def get_auth_url():
    AppID = 'wx9265cb5f7f0ccaaa'
    AppSecret = 'c3f932c5958aaebc31b4bfd82a657318'
    wechat_auth_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={' \
                      '1}&response_type=code&scope=snsapi_base#wechat_redirect'.format(
        AppID, 'http://113.16.255.12:11029')

    return wechat_auth_url

if __name__ == '__main__':
    print(get_auth_url())
