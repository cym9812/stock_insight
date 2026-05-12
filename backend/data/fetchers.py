import logging

from backend.data.storage import FeatureStoreManager

logger = logging.getLogger(__name__)


# 此处假设上游 SDK 提供了 query_snapshot 函数
# from upstream_sdk import query_snapshot

def sync_stock_data(code_list: list[str], store_manager: FeatureStoreManager):
    """
    全量同步股票数据：
    1. 调用上游 query_snapshot 获取全量数据（利用 SDK 自身的 is_local=True 缓存加速机制）
    2. 将返回的数据重新落盘为我们的独立 Parquet 格式，供 DuckDB 查询。
    """
    try:
        # TODO: 替换为实际的 SDK 调用。为了跑通业务，使用全量同步。
        # 伪代码：
        # snapshot_dict = query_snapshot(
        #     code_list=code_list, 
        #     local_path=str(settings.DATA_STORE_PATH), 
        #     is_local=True
        # )

        # 示例：假装得到了 snapshot_dict
        snapshot_dict = {}  # key: ticker, value: DataFrame

        for ticker, df in snapshot_dict.items():
            if not df.empty:
                logger.info(f"Syncing data for {ticker}, rows: {len(df)}")
                store_manager.append_stock_data(ticker, df)

    except Exception as e:
        logger.error(f"Failed to sync stock data: {e}")
        raise e
