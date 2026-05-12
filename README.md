# Stock Analysis Platform (Stock Insight)

这是一个基于 FastAPI 和 Vue 3 的本地化股票量化分析与大模型交互平台。

## 项目结构

```text
stock_insight/
├── backend/            # Python 后端 (FastAPI)
├── frontend/           # Vue 3 前端 (Vite + TS)
├── local_data/         # 本地 Parquet 特征仓库
└── pyproject.toml      # 后端依赖配置
```

## 快速开始

### 1. 后端启动

确保已安装 Python 3.12+。推荐使用 `uv` 管理：

```bash
# 安装依赖 (如果尚未安装)
pip install -e .

# 启动后端
python -m backend.main
```
后端 API 将运行在 `http://localhost:8000`。

### 2. 前端启动

```bash
cd frontend
npm install
npm run dev
```
前端应用将运行在 `http://localhost:5173`。

## 核心功能 (已搭建脚手架)

- **数据底座**：基于 Parquet 的本地特征仓库 (`backend/data/storage.py`)。
- **配置管理**：使用 Pydantic Settings 实现全局路径与环境配置。
- **AI Agent**：预留大模型交互接口 (`backend/api/endpoints_agent.py`)。
- **现代化 UI**：使用 Vue 3 搭建的极简深色系管理后台。

## 许可证
MIT
