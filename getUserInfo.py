import vrchatapi
import os
from vrchatapi.api import authentication_api
from vrchatapi.api import users_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode
from dotenv import load_dotenv
from auth import create_api_client


# .envファイルを読み込む
load_dotenv()

# APIクライアントを作成
try:
    api_client = create_api_client()
except vrchatapi.ApiException as e:
    print("APIクライアント作成失敗")
    print("Exception when calling API: %s\n", e)
    exit(1)

# envから読み込んだUSER_IDを指定してユーザ情報を取得
try:
    print("指定したユーザー情報を取得")
    user_id = os.getenv('VRC_USER_ID')
    users_api = users_api.UsersApi(api_client)
    user = users_api.get_user(user_id=user_id)
    print(user)
except vrchatapi.ApiException as e:
    print("ユーザ情報取得API実行失敗")
    print("Exception when calling API: %s\n", e)