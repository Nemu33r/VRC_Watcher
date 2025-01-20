import discord
import config
import random
import vrchatapi
import os
import asyncio
from discord import app_commands
from discord import Object
from auth import create_api_client
from auth import check_auth
from getWorldInfo import get_world_info
from logger import logger

# インテントの設定
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Botのインスタンス化
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# グローバル変数として扱う値の定義
api_client = None
watch_user = None
watch_world = None

# タスク管理用のグローバル変数
world_task = None

# Bot起動時に呼び出される関数
@client.event
async def on_ready():
    global api_client
    try:
        api_client = create_api_client()
    except vrchatapi.ApiException as e:
        logger.error("APIクライアント作成失敗")
        logger.error("Exception when calling API: %s\n", e)
        exit(1)
    try:
        # Botのステータスを変更
        new_activity = f"電子の海"
        await client.change_presence(activity=discord.Game(name=new_activity))
        
        # スラッシュコマンドの同期
        await tree.sync()
        await tree.sync(guild=Object(id=os.getenv("GUILD_ID")))
    except Exception as e:
        logger.error("初期設定に失敗")
        logger.error("Exception when calling API: %s\n", e)
        exit(1)
    logger.info("Ready!")


# メッセージの検知
@client.event
async def on_message(message):
    # 自身が送信したメッセージには反応しない
    if message.author == client.user:
        return

    # ユーザーからのメンションを受け取った場合、あらかじめ用意された配列からランダムに返信を返す
    if client.user in message.mentions:

        ansewr_list = ["さすがですね！","知らなかったです！","すごいですね！","センスが違いますね！","そうなんですか？"]
        answer = random.choice(ansewr_list)
        print(answer)
        await message.channel.send(answer)

@tree.command(name="hello", description="挨拶を返します")
async def hello(interaction: discord.Interaction):
    logger.info("Hello World!")
    await interaction.response.send_message("Hello World!")

# 指定されたワールドIDのワールド情報を取得して表示する
@tree.command(name="getworld", description="ワールド情報を取得します", guild=Object(id=os.getenv("GUILD_ID")))
async def getworld(interaction: discord.Interaction, world_id: str):
    try:
        logger.info("ワールド情報取得コマンドを受信、処理開始")
        logger.info("ワールドID: %s", world_id)
        global api_client, watch_world
        watch_world = world_id
        world_info = get_world_info(api_client, world_id)
        await interaction.response.send_message(world_info)
    except vrchatapi.ApiException as e:
        logger.error("ワールド情報取得に失敗")
        logger.error("Exception when calling API: %s\n", e)
        if e.status == 404:
            await interaction.response.send_message("指定したワールドが存在しませんでした。")
        elif e.status == 429:
            await interaction.response.send_message("APIのリクエスト制限に達しました。")
        else:
            await interaction.response.send_message("ワールド情報が取得できませんでした。管理者にお問い合わせください。")
        
# 指定されたワールドIDのワールド情報を定期的に取得して表示する
@tree.command(name="setworld", description="ワールド情報を定期的に取得します", guild=Object(id=os.getenv("GUILD_ID")))
async def setworld(interaction: discord.Interaction, world_id: str, interval_min: int):
    global api_client, watch_world, world_task
    watch_world = world_id
    
    # 定期的にワールド情報を取得するタスク
    async def fetch_world_info():
        while True:
            logger.info("定期ワールド情報取得開始")
            world_info = get_world_info(api_client, world_id)
            if world_info:
                await interaction.channel.send(world_info)
                logger.info("定期ワールド情報取得完了、次回実行までSleep")
            else:
                await interaction.channel.send("ワールド情報の取得に失敗しました。")
                logger.info("ワールド情報取得失敗。次回実行までSleep")
            await asyncio.sleep(interval_min * 60)
            
    # 既存のタスクがあればキャンセル
    if world_task is not None:
        world_task.cancel()

    # 新しいタスクを作成して実行
    logger.info("定期ワールド情報取得コマンドを受信。タスクを作成")
    logger.info("ワールドID: %s, 間隔: %s分", world_id, interval_min)
    world_task = client.loop.create_task(fetch_world_info())
    await interaction.response.send_message(f"ワールド情報の定期取得を開始しました。ワールドID: {world_id}, 間隔: {interval_min}分")

# 定期取得を停止するコマンド
@tree.command(name="stopworld", description="ワールド情報の定期取得を停止します", guild=Object(id=os.getenv("GUILD_ID")))
async def stopworld(interaction: discord.Interaction):
    global world_task
    if world_task is not None:
        logger.info("定期ワールド情報取得停止コマンドを受信。停止開始")
        world_task.cancel()
        world_task = None
        logger.info("定期ワールド情報取得停止完了")
        await interaction.response.send_message("ワールド情報の定期取得を停止しました。")
    else:
        logger.info("タスクが存在しないため定期取得停止処理をスキップ")
        await interaction.response.send_message("定期取得は実行されていません。")

# 認証状態を確認し、切れていた場合は再認証を行う
@tree.command(name="checkauth", description="認証状態を確認します", guild=Object(id=os.getenv("GUILD_ID")))
async def checkauth(interaction: discord.Interaction):
    global api_client
    try: 
        name = check_auth(api_client)
        if name:
            logger.info("認証状態の確認に成功")
            await interaction.response.send_message(f"認証状態は正常です。ユーザ名：{name}")
        else:
            logger.info("認証状態の確認に失敗、再認証を実施")
            await interaction.response.send_message("認証状態が切れています。再認証を実施")
            api_client = create_api_client()            
    except vrchatapi.ApiException as e:
        logger.error("認証状態の確認、もしくは再認証に失敗")
        logger.error("Exception when calling API: %s\n", e)
        await interaction.response.send_message("認証状態が不正、もしくは再認証に失敗しました") 

# Bot起動
client.run(config.DISCORD_TOKEN)
