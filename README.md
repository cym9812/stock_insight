# Stock Analysis Platform (Stock Insight)

这是一个基于 FastAPI 和 Vue 3 的本地化股票量化分析与大模型交互平台。

## 项目结构

```text
stock_insight/
├── backend/                    # Python 后端 (FastAPI)
│   ├── api/                    # API 路由层，只处理 HTTP 入参和响应
│   │   ├── router.py           # API v1 总路由
│   │   └── v1/                 # 按业务拆分的接口模块
│   ├── services/               # 业务编排层
│   ├── schemas/                # Pydantic 响应模型
│   ├── core/                   # 配置、日志等应用基础设施
│   ├── data/                   # 本地数据仓、标准化、数据源适配接口
│   ├── docs/                   # SDK/API 参考文档
│   ├── deps/                   # 本地 wheel 依赖
│   └── tests/                  # 后端测试
├── frontend/                   # Vue 3 前端 (Vite + TS)
│   └── src/
│       ├── api/                # 前端接口访问层
│       ├── types/              # 前端类型定义
│       ├── views/              # 页面
│       ├── components/         # 通用组件
│       └── assets/             # 静态资源
├── local_data/                 # 本地数据根目录，运行时自动创建且不提交
│   ├── source_data/            # 原始采集数据
│   ├── normalized_data/        # 标准化数据
│   ├── derived_data/           # 派生计算数据
│   ├── application_data/       # 应用直接消费的数据
│   ├── metadata/               # 数据说明、schema、同步记录
│   ├── databases/              # 本地数据库与索引
│   ├── artifacts/              # 回测、模型、报告、导出等产物
│   ├── cache/                  # 可删除缓存
│   └── temporary/              # 临时文件
├── pyproject.toml              # 后端依赖配置
└── uv.lock                     # uv 锁文件
```

## 快速开始

### 1. 后端启动

确保已安装 Python 3.12+。推荐使用 `uv` 管理：

```bash
# 安装依赖 (如果尚未安装)
uv sync

# 启动后端
uv run python -m backend.main
```
后端 API 将运行在 `http://localhost:18000`。

### 2. 前端启动

```bash
cd frontend
npm install
npm run dev
```
前端应用将运行在 `http://localhost:5173`。

## API 路由

- `GET /api/v1/stocks`
- `GET /api/v1/stocks/{ticker}/bars`
- `GET /api/v1/stocks/{ticker}/analysis`
- `GET /api/v1/market/sentiment`
- `GET /api/v1/market/indices`
- `GET /api/v1/market/heatmap`
- `GET /api/v1/strategies/recommendations`
- `GET /api/v1/strategies/backtest`
- `GET /api/v1/portfolio/overview`
- `POST /api/v1/agent/chat`

## 初始框架

- **数据底座**：基于 Parquet 的本地标准化行情存储 (`backend/data/market_bar_store.py`)。
- **数据标准化**：统一行情字段、时间和空值处理 (`backend/data/normalizers.py`)。
- **数据源接口**：以 `backend/data/providers/base.py` 作为真实行情源适配入口。
- **数据目录布局**：以 `backend/data/layout.py` 统一管理 `local_data` 下的各类运行期数据目录。
- **后端分层**：API / Services / Schemas / Data 分离，便于后续接真实 SDK、策略和 Agent。
- **前端分层**：页面通过 `frontend/src/api` 访问后端，通过 `frontend/src/types` 共享业务类型。
- **配置管理**：使用 Pydantic Settings 实现全局路径、环境变量、运行参数配置。
- **日志系统**：使用 Loguru 提供控制台日志、文件日志、轮转和保留策略。
- **本地数据**：`local_data` 为运行期目录，由服务自动创建，不提交到仓库。

## 本地数据规范

`local_data` 是本地运行期数据根目录，用于存放采集、清洗、计算和应用缓存产生的数据。该目录由服务启动时自动创建，不提交到仓库。

- `source_data`：原始采集数据。第三方 SDK/API 返回什么就保存什么，尽量不修改、不覆盖。
- `normalized_data`：标准化数据。项目统一字段名、时间格式、股票代码格式和空值规则后的数据。
- `derived_data`：派生计算数据。由标准化数据计算得到的技术指标、因子、文本特征、策略信号等。
- `application_data`：应用直接消费的数据。面向接口和前端的聚合结果、快照和用户工作区数据。
- `metadata`：数据说明。包含数据集登记、schema、同步记录、质量检查和数据血缘信息。
- `databases`：本地数据库与索引。用于 DuckDB、SQLite、全文检索索引等文件。
- `artifacts`：运行产物。包含回测结果、模型文件、报告和导出文件。
- `cache`：可删除缓存。用于加速运行，不作为可信数据源。
- `temporary`：临时文件。用于单次任务的中间文件，任务结束后可清理。

## 许可证
MIT
