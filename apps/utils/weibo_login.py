def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_url = 'http://113.16.255.12:11029/complete/weibo/'
    auth_url = weibo_auth_url + '?client_id={0}&redirect_url={1}'.format("1782512147", 'http://113.16.255.12:11029/')

    print(auth_url)


def get_access_token():
    pass


if __name__ == '__main__':
    get_auth_url()