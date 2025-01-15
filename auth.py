import vrchatapi
import os
from vrchatapi.api import authentication_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode
from dotenv import load_dotenv

def create_api_client():
    print("認証情報を.envから読み出して設定")
    load_dotenv()
    configuration = vrchatapi.Configuration(
        username = os.getenv("VRC_USERNAME"),
        password = os.getenv("VRC_PASSWORD"),
    )
    api_client = vrchatapi.ApiClient(configuration)
    api_client.user_agent = f"Mozilla/5.0 {configuration.username}"
    auth_api = authentication_api.AuthenticationApi(api_client)
    
    try:
        print("ログイン状態の確認")
        current_user = auth_api.get_current_user()
        print(f"Logged in as: {current_user.display_name}")
        return api_client
    except UnauthorizedException as e:
        if e.status == 200:
            try:
                auth_api.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(input("Email 2FA Code: ")))
                print("2FAメールコードの検証に成功")
                return api_client
            except vrchatapi.ApiException as e:
                print("2FAメールコードの検証に失敗")
                print("Exception when calling API: %s\n", e)
                raise e 
        elif "2 Factor Authentication" in e.reason:
            try:
                auth_api.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(input("2FA Code: ")))
                print("2FAコードの検証に成功")
                return api_client
            except vrchatapi.ApiException as e:
                print("2FAコードの検証に失敗")
                print("Exception when calling API: %s\n", e)
                raise e
        else:
            print("例外が発生")
            print("Exception when calling API: %s\n", e)
            raise e