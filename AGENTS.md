# AGENTS.md

本文档面向参与本项目开发的协作者和代码代理，用于说明当前项目状态、目录职责、开发命令和协作约定。

## 项目定位

Stock Insight 是一个本地化股票量化分析与大模型交互平台。

当前项目处于正式开发初始阶段，目标是先建立清晰、可扩展、无演示包袱的基础框架。现阶段不接入真实行情 SDK 和真实大模型服务，真实数据源后续应通过明确的 provider 接口接入。

## 当前技术栈

- 后端：FastAPI、Pydantic Settings、Loguru、DuckDB、Pandas、PyArrow。
- 前端：Vue 3、Vite、TypeScript、Vue Router、Axios、ECharts。
- Python 环境与命令：使用 `uv`。
- 本地数据：以 `local_data` 作为本地运行期数据根目录，目录由服务启动时自动创建，真实数据默认不提交。

## 必须遵守

- 忽略 `html/` 目录，不把它作为当前项目结构、代码质量或架构判断依据。
- 后端命令必须使用 `uv run`，例如 `uv run python -m unittest discover backend\tests`。
- 不要恢复旧演示代码、旧 mock 数据、旧 `feature_store` 命名或旧 `/api/v1/data/...` 路由。
- 不要直接把真实 SDK 调用写进 API 层或 service 层，应先通过 `backend/data/providers/` 的接口接入。
- 不要把运行期数据目录、日志、缓存、数据库文件提交到仓库。
- 新增代码优先保持小而清晰，避免提前引入 Nacos、热更新、HPC 队列等与当前项目无关的复杂设施。

## 后端结构

```text
backend/
├── api/                 # API 路由层，只处理 HTTP 入参和响应
│   ├── router.py        # API v1 总路由
│   └── v1/              # 按业务拆分的接口模块
├── services/            # 业务编排层
├── schemas/             # Pydantic 响应模型
├── core/                # 配置、日志等应用基础设施
├── data/                # 本地数据存储、标准化、数据源适配接口
├── docs/                # SDK/API 参考文档
├── deps/                # 本地 wheel 依赖
└── tests/               # 后端测试
```

主要模块：

- `backend/main.py`：FastAPI 应用入口，挂载 CORS、健康检查和 API v1 路由。
- `backend/core/config.py`：全局配置，基于 Pydantic Settings，从环境变量读取。
- `backend/core/logging.py`：Loguru 日志初始化，接管标准库 logging。
- `backend/data/layout.py`：统一管理 `local_data` 目录布局。
- `backend/data/market_bar_store.py`：标准化行情 K 线的本地 Parquet 存储。
- `backend/data/normalizers.py`：行情字段、时间和空值标准化。
- `backend/data/providers/base.py`：真实行情数据源适配接口。

## 前端结构

```text
frontend/src/
├── api/          # 前端接口访问层
├── types/        # 业务类型定义
├── views/        # 页面
├── components/   # 通用组件
├── config/       # 前端配置
└── router/       # 路由
```

前端页面应通过 `frontend/src/api` 访问后端，不要在视图中硬编码请求细节。业务数据类型放在 `frontend/src/types`。

## 本地数据目录规范

`local_data` 是本地运行期数据根目录，由服务启动时自动创建，真实数据默认不提交。

```text
local_data/
├── source_data/          # 原始采集数据
├── normalized_data/      # 标准化数据
├── derived_data/         # 派生计算数据
├── application_data/     # 应用直接消费的数据
├── metadata/             # 数据说明、schema、同步记录
├── databases/            # 本地数据库与索引
├── artifacts/            # 回测、模型、报告、导出等产物
├── cache/                # 可删除缓存
└── temporary/            # 临时文件
```

放置规则：

- `source_data`：第三方 SDK/API 返回的原始数据，尽量不修改、不覆盖。
- `normalized_data`：统一字段名、时间格式、股票代码格式和空值规则后的数据。
- `derived_data`：技术指标、因子、文本特征、策略信号等计算结果。
- `application_data`：面向接口和前端的聚合结果、快照和用户工作区数据。
- `metadata`：数据集登记、schema、同步记录、质量检查和数据血缘信息。
- `databases`：DuckDB、SQLite、全文检索索引等本地数据库文件。
- `artifacts`：回测结果、模型文件、报告和导出文件。
- `cache`：可删除缓存，不作为可信数据源。
- `temporary`：单次任务的临时文件。

当前标准化行情 K 线默认存储在：

```text
local_data/normalized_data/market_bars/
```

## API 路由

当前 API v1 路由：

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

## 开发命令

后端：

```bash
uv sync
uv run python -m backend.main
uv run python -m compileall backend
uv run python -m unittest discover backend\tests
uv run ruff check backend
```

前端：

```bash
cd frontend
npm install
npm run dev
npm run build
```

## 配置

配置样例见 `.env.example`。

重要环境变量：

- `PROJECT_NAME`
- `ENVIRONMENT`
- `API_V1_PREFIX`
- `APP_HOST`
- `APP_PORT`
- `APP_RELOAD`
- `CORS_ORIGINS`
- `DATA_ROOT_PATH`
- `LOG_LEVEL`
- `LOG_TO_FILE`
- `LOG_DIR`

## 编码约定

- API 层只做请求参数处理、响应模型组织和调用 service。
- Service 层负责编排业务逻辑，不直接散落第三方 SDK 调用。
- Data 层负责数据目录、存储、标准化、provider 接口和数据读写。
- Schema 层定义接口响应和业务数据结构。
- 配置统一从 `backend/core/config.py` 获取。
- 日志使用 `loguru`，初始化入口在 `backend/core/logging.py`。
- 本地数据路径统一通过 `backend/data/layout.py` 获取。

## 当前边界

- 真实行情 SDK 尚未接入。
- Agent 服务尚未接入真实大模型。
- 市场情绪、策略推荐、投资组合等接口目前只保留正式接口形状，不提供伪造业务数据。
- 当前测试覆盖基础数据标准化、本地行情存储和主要 API 路由可用性。

## 修改前检查

开始修改前建议先运行：

```bash
git status --short
rg -n "FeatureStoreManager|feature_store|DATA_STORE_PATH|/api/v1/data|old-kline|demo|Mock" -g "!html/**"
```

提交或交付前建议运行：

```bash
uv run python -m compileall backend
uv run python -m unittest discover backend\tests
uv run ruff check backend
cd frontend
npm run build
```
