import uuid

from myapp.ResponseHandler import ResponseHandler
from myapp.factory import ModelAPIFactory
from myapp.config import load_config

def main():
    # 示例配置路径
    config_path = "config.json"

    # 加载配置文件
    config = load_config(config_path)

    # 选择API
    api_type = "mify"
    api_config = config["apis"][api_type]

    # 打印 api_key 进行调试
    print(f"API Key: {api_config['api_key']}")

    # 创建API实例
    model_api = ModelAPIFactory.create_model_api(api_type, api_config)

    # response_mode : streaming or blocking
    try:
        # 发送消息
        events = model_api.send_message(
            query="What is the capital of France?",
            inputs={},
            response_mode="streaming",
            user="shichunming",
            conversation_id=None,
            files=None,
            auto_generate_name=True
        )

        # 检查事件列表是否为空
        if not events:
            raise ValueError("Empty response events")
        # 生成会话 ID
        conversation_id = uuid.uuid4()
        # 创建 ResponseHandler 实例
        handler = ResponseHandler(events)
        # 保存到数据库
        handler.save_to_database()
        # 流式展示
        print("\nStreamed Response:")
        handler.show_stream()

    except Exception as e:
        print(f"main_An error occurred: {e}")


if __name__ == "__main__":
    main()