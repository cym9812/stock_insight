from pathlib import Path

from pydantic_settings import BaseSettings

# 获取项目根目录 (假设运行在 stock_insight 下)
# 目录结构：
# stock_insight/
# ├── backend/
# │   └── config.py
# └── local_data/
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "Stock Analysis Platform"
    API_V1_STR: str = "/api/v1"

    # 本地特征仓库路径
    DATA_STORE_PATH: Path = BASE_DIR / "local_data" / "feature_store"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
