import logging
import os

# ログレベルの設定
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# ロガーの設定
logger = logging.getLogger("VRC_Watcher")
logger.setLevel(log_level)

# コンソールハンドラの設定
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# フォーマッタの設定
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# ハンドラをロガーに追加
logger.addHandler(console_handler)

# ファイルハンドラの設定
file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)

# ファイルハンドラをロガーに追加
logger.addHandler(file_handler)