import axios from 'axios'
import { API_BASE } from '../config/api'

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
})
