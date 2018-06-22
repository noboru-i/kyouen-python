export const state = () => ({
  list: []
})

export const mutations = {
  setListStages(state, {stages}) {
    state.list = stages;
  }
}

export const actions = {
  async fetchListStages({commit}, page) {
    const stages = await this.$axios.$get('/api/stages?page_no=' + page)
    commit('setListStages', {stages});
  }
}
