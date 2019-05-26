from random import Random

from django.core.mail import send_mail

from MxShop.settings import EMAIL_FROM


# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, code=None, send_type='register'):
    if not code:
        code = random_str(16)

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'MxOnline注册激活链接'
        email_body = '点击以下链接激活账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == "forget":
        email_title = "MxOnline找回密码链接"
        email_body = "请点击下面的链接找回你的密码：http://127.0.0.1:8000/reset/{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass

    if send_type == "update_email":
        email_title = "MxOnline修改邮箱验证码"
        email_body = "你的邮箱验证码为{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass


if __name__ == '__main__':
    send_register_email('lhsheild@sina.com', code=1234)
