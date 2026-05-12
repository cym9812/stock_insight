/**
 * 全局 API 配置
 * 所有视图统一从此处引用后端地址，便于环境切换和统一管理
 */
export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:18000/api/v1'
export const API_DATA = `${API_BASE}/data`
export const API_AGENT = `${API_BASE}/agent`
