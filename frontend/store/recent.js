export const state = () => ({
  list: []
})

export const mutations = {
  setRecentStages(state, {stages}) {
    state.list = stages;
  }
}

export const actions = {
  async fetchRecentStages({commit}) {
    const stages = await this.$axios.$get('/api/recent_stages')
    commit('setRecentStages', {stages});
  }
}
