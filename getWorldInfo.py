import json
from vrchatapi.api import worlds_api
from vrchatapi.exceptions import ApiException
from logger import logger
############################################
#  get_world_info
#  指定したワールド情報を取得する関数
#   引数:
#     api_client: APIクライアント
#     world_id: ワールドID
#   戻り値:
#     world_info: ワールド情報
############################################
def get_world_info(api_client, world_id):
    # 指定したワールド情報を取得
    try:
        logger.info("指定したワールド情報を取得")
        worlds_api_instance = worlds_api.WorldsApi(api_client)
        world = worlds_api_instance.get_world(world_id=world_id)
        # 取得した情報から欲しい情報だけを切り出す
        name = world.name
        private_occupants = world.private_occupants
        public_occupants = world.public_occupants
        world_info = {
            "name": name,
            "private_occupants": private_occupants,
            "public_occupants": public_occupants
        }
        
        logger.info(f"取得したワールド情報: {world_info}")
        
        return json.dumps(world_info, ensure_ascii=False)
    except ApiException as e:
        logger.info("ワールド情報取得API実行失敗")
        logger.info("Exception when calling API: %s\n", e)
        return None