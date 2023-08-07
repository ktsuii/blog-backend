"""
666资源站-每日签到
@Date: 2023-04-16
@Author: zhouziling
@attention: 2023-08-04 网站已经停止运营
"""
from dataclasses import dataclass, asdict
from enum import Enum

from settings import Config
from lxml import etree
from base import BaseSpider
from logger import info_log


class Const(Enum):
    USER_LOGIN = 'user_login'
    USER_SIGNIN = 'qiandao'
    BALANCE_XPATH = '//div[@class="author-info mcolorbg4"]/h3/text()'


@dataclass
class LoginReqParam:
    action: str
    username: str
    password: str


@dataclass
class SigninReqParam:
    action: str


class ResourceSix(BaseSpider):

    def _require(self):
        self.index_url = Config.resource_six_index_url
        self.user_url = Config.resource_six_user_url
        self.login_data = LoginReqParam(
            action=Const.USER_LOGIN.value,
            username=Config.resource_six_username,
            password=Config.resource_six_password
        )
        self.signin_data = SigninReqParam(action=Const.USER_SIGNIN.value)

    def run(self):
        """
        1. 登录
        2. 签到
        3. 检查余额
        """
        resp_login = self.request('POST', self.index_url, data=asdict(self.login_data))
        if resp_login is None:
            raise ValueError('login failed, please check...')

        self.session.cookies.update(resp_login.cookies)

        resp_signin = self.request('POST', self.index_url, data=asdict(self.signin_data))
        if resp_signin is None:
            raise ValueError('signin failed, please check...')

        resp_balance = self.request('GET', self.user_url)
        if resp_balance is None:
            raise ValueError('get balance failed, please check...')

        htm = etree.HTML(resp_balance.text)
        balance = htm.xpath(Const.BALANCE_XPATH.value)[0]
        info_log.info(f"sign in success, current balance: {balance}")


if __name__ == '__main__':
    ResourceSix().main()
