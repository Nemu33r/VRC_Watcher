import vrchatapi
import os
from vrchatapi.api import users_api
from dotenv import load_dotenv
from auth import create_api_client
from logger import logger

# .envファイルを読み込む
load_dotenv()

# APIクライアントを作成
try:
    api_client = create_api_client()
except vrchatapi.ApiException as e:
    logger.error("APIクライアント作成失敗")
    logger.error("Exception when calling API: %s\n", e)
    exit(1)

# envから読み込んだUSER_IDを指定してユーザ情報を取得
try:
    logger.info("指定したユーザー情報を取得")
    user_id = os.getenv('VRC_USER_ID')
    users_api = users_api.UsersApi(api_client)
    user = users_api.get_user(user_id=user_id)
    logger.info(user)
except vrchatapi.ApiException as e:
    logger.error("ユーザ情報取得API実行失敗")
    logger.error("Exception when calling API: %s\n", e)