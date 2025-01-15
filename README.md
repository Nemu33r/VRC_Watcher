# VRC_Watcher

VRC_Watcherは、VRChatのワールドを監視するためのBotです。

## 機能

- VRChat APIを使用して各種情報の取得
- 定期的に設定した情報をウォッチし、差分があった場合通知します(作成中……)。  
設定情報はユーザ、ワールド単位を予定しています。

## 注意事項
- VRChat APIの仕様上、1req/min以上の頻度でリクエストを送付すると429としてエラー応答が帰ります。  
クロール頻度は調整可能(予定)ですが、それ以上の頻度で実行することはお控えください。


## インストール

- 事前にDiscord DevにてBotを作成してください。作者から動作させるサーバやBotの提供予定はございません。
- 作成したBotのTokenを払い出し、.envに`DISCORD_TOKEN`として設定してください。

1. リポジトリをクローンします。

    ```sh
    git clone https://github.com/yourusername/VRC_Watcher.git
    cd VRC_Watcher
    ```

2. 仮想環境を作成し、必要なパッケージをインストールします。

    ```sh
    python -m venv venv
    source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. `.env`ファイルを作成し、必要な環境変数を設定します。

    ```env
    DISCORD_TOKEN=your_bot_token
    VRC_USERNAME=your_vrchat_username
    VRC_PASSWORD=your_vrchat_password
    ```

## 使用方法

1. Botを起動します。

    ```sh
    python main.py
    ```

2. を実行してユーザー情報を取得します。

    ```sh
    python getUserInfo.py
    ```

## 環境変数
- `DISCORD_TOKEN`：通知させるDiscord Botのトークン
- `VRC_USERNAME`: VRChatのユーザー名
- `VRC_PASSWORD`: VRChatのパスワード

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細はファイルを参照してください。
