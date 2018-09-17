from flask import Flask, request
import proxyhelper
import config
import threading
import time


def execute():
    threading.Thread(target=_update_proxy_daily).start()
    app = Flask(__name__)

    @app.route('/')
    def index():
        qr_img_base64 = 'data:image/jpeg;base64,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PSv5WQa/qmAxQB/Kz+NGPev6p6Q9KAAdKK/lYPWigD+qdunSv5WyAKZ0r+qfFACLX8rNf1T9MV/KxQB/VOeaTbX8rNFAH9UxJBxX8rJGDQDignJoA/qnJIHSv5WioHf86b0r+qfHWgBueenX1pw5HSv5Wc1/VMBigBaKKKACiiigAooooATvX8rFf1T96/lYoA/qor+VftX9U5OK/lZIoASijFGKAP6qK/lX9K/qor+Vf0oA/qnzjFfysEYNf1TFc4pQCABmgBa/lY9K/qmyBX8rPSgD+qbPSv5WOlODAdq/qlAIHWgAJwKAQelfysjr0r+qRRzn26UAOJA60A5FIy5PXtX8rWR6UAIBk1/VODmkPIIzQBtNACkgdaAcikIya/layPSgD+qekPSv5WfwpenagBPWv6putNIr+Vs9elACV/VP0zX8rFf1TkUALRX8rBIz0oz7UAIBk1/VODmggkEZpAuDQAvev5WK/qn71/KxQB/VRX8q/XFf1T5r+VrGKAG4oIwa/qlOev6V/K2Rz0/KgD+qeiiigAooooAKKKKAE71/KxX9U/ev5WKAP6pzzQBiv5WKKAP6p8ewox7Cv5WKKAP6pySBnGa/lZIxg+9IDg0ZJNAH9U46UtIOlLQB/KvmgknrRRQAdq/qor+VftX9VFACEA0Y29KWkPSgBpYg9K/lbIHrR61/VN0oA/lYHJ607HGc00HFf1TgCgBu7Bxj8a/lbwPWv6pto9KAMCgAI46V/K1jjPHWv6pSMjBoxgUANJzxinAcdK/lZzX9UwGKAP5WK/qnJr+Viv6p+uaAP5Wto6+9NIwa/qnIFfysE5oA/qnor+ViigD+qYsQelfytED1pBX9U/SgD+Vkdetf1SA896cRkUYAFACYz1pQMdq/lYPWigD+qiiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/2Q=='
        contents = [
            'github:<a href="https://github.com/LuChuanBing/free-proxy-pool">https://github.com/LuChuanBing/free-proxy-pool</a>',
            '作者/Author: bingge',
            '联系方式/contact: 微信公众号:<b>高效工具库(gaoxiaogongjuku)</b>',
            "<img alt='微信公众号:gaoxiaogongjuku'  src='{}' />".format(qr_img_base64),
            '当前共有<b>{}</b>个代理IP'.format(proxyhelper.get_proxy_count()),
            "<a href='https://github.com/LuChuanBing/free-proxy-pool/blob/master/README.md'>说明文档</a>",
            "<a href='https://github.com/LuChuanBing/free-proxy-pool/blob/master/README.en.md'>readme</a>"
        ]
        return '<div style="margin:10px"></div>'.join(contents)

    @app.route('/get')
    def get(protocol='http', token=None):
        if request.values.get('protocol') not in ['http', 'https']:
            protocol = request.values.get('protocol')
        if request.values.get('token'):
            token = request.values.get('token')
        proxy = proxyhelper.next(protocol, token)
        return proxy['proxy_addr']

    @app.route('/get_all')
    def get_all(protocol='http', token=None):
        if not request.values.get('token'):
            return '请先关注微信公众号   高效工具库(gaoxiaogongjuku) 获取token'
        if request.values.get('protocol') in ['http', 'https']:
            protocol = request.values.get('protocol')
        token = request.values.get('token')
        proxies = proxyhelper.get_all(protocol, token)
        return str(map(lambda proxy: proxy['proxy_addr'], proxies))

    app.run(host=config.webapi_host, port=config.webapi_port)


def _update_proxy_daily():
    while True:
        proxyhelper.update_proxy()
        time.sleep(24 * 60 * 60)
