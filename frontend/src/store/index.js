import { createStore } from 'vuex'
import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL

export default createStore({
  state: {
    servers: [],
    loading: false,
    error: null
  },
  
  mutations: {
    SET_SERVERS(state, servers) {
      state.servers = servers
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    ADD_SERVER(state, server) {
      state.servers.push(server)
    },
    UPDATE_SERVER(state, { index, server }) {
      state.servers[index] = server
    },
    DELETE_SERVER(state, index) {
      state.servers.splice(index, 1)
    }
  },
  
  actions: {
    async fetchServers({ commit }) {
      try {
        commit('SET_LOADING', true)
        const response = await axios.get(`${API_URL}/api/mappings`)
        commit('SET_SERVERS', response.data)
        commit('SET_ERROR', null)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async addServer({ commit }, server) {
      try {
        commit('SET_LOADING', true)
        await axios.post(`${API_URL}/api/mappings`, server)
        commit('ADD_SERVER', server)
        commit('SET_ERROR', null)
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async updateServer({ commit, state }, { name, server }) {
      try {
        commit('SET_LOADING', true)
        await axios.put(`${API_URL}/api/mappings/${name}`, server)
        const index = state.servers.findIndex(s => s.name === name)
        if (index !== -1) {
          commit('UPDATE_SERVER', { index, server })
        }
        commit('SET_ERROR', null)
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async deleteServer({ commit, state }, name) {
      try {
        commit('SET_LOADING', true)
        await axios.delete(`${API_URL}/api/mappings/${name}`)
        const index = state.servers.findIndex(s => s.name === name)
        if (index !== -1) {
          commit('DELETE_SERVER', index)
        }
        commit('SET_ERROR', null)
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async toggleServer({ dispatch }, name) {
      try {
        await axios.post(`${API_URL}/api/mappings/${name}/toggle`)
        await dispatch('fetchServers')
      } catch (error) {
        throw error
      }
    }
  }
}) 