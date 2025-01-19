import vrchatapi
import os
from vrchatapi.api import authentication_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode
from dotenv import load_dotenv
from generate_TOTP import generate_TOTP
from logger import logger

############################################
#  create_api_client
#  APIクライアントを生成する関数
#   引数:
#     なし
#   戻り値:
#     api_client: APIクライアント
############################################
def create_api_client():
    logger.info("認証情報を.envから読み出して設定")
    load_dotenv()
    configuration = vrchatapi.Configuration(
        username = os.getenv("VRC_USERNAME"),
        password = os.getenv("VRC_PASSWORD"),
    )
    api_client = vrchatapi.ApiClient(configuration)
    api_client.user_agent = f"Mozilla/5.0 {configuration.username}"
    auth_api = authentication_api.AuthenticationApi(api_client)
    
    try:
        logger.info("ログイン状態の確認")
        current_user = auth_api.get_current_user()
        logger.info(f"Logged in as: {current_user.display_name}")
        return api_client
    except UnauthorizedException as e:
        logger.info("ログイン状態の確認に失敗")
        if "2 Factor Authentication" in e.reason:
            try:
                logger.info("2FAコードの取得")
                code = generate_TOTP()
                logger.info(f"2FAコード: {code}")
                auth_api.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(code))
                logger.info("2FAコードの検証に成功")
                return api_client
            except vrchatapi.ApiException as e:
                logger.error("ログイン失敗：2FAコードの検証に失敗")
                logger.error("Exception when calling API: %s\n", e)
                raise e
        elif e.status == 200:
            try:
                auth_api.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(input("Email 2FA Code: ")))
                logger.info("2FAメールコードの検証に成功")
                return api_client
            except vrchatapi.ApiException as e:
                logger.error("ログイン失敗：2FAメールコードの検証に失敗")
                logger.error("Exception when calling API: %s\n", e)
                raise e 
        else:
            logger.error("ログイン失敗：例外が発生")
            logger.error("Exception when calling API: %s\n", e)
            raise e

############################################
#  check_auth
#  ログイン状態を確認する関数
#   引数:
#     api_client: APIクライアント
#   戻り値:
#     current_user.display_name: ユーザー名
############################################

def check_auth(api_client):
    try:
        auth_api = authentication_api.AuthenticationApi(api_client)
        current_user = auth_api.get_current_user()
        logger.info(f"Logged in as: {current_user.display_name}")
        return current_user.display_name
    except UnauthorizedException as e:
        logger.info("ログイン状態の確認に失敗")
        logger.info("Exception when calling API: %s\n", e)
        raise e