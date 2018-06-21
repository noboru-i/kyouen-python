export const state = () => ({
  list: []
})

export const mutations = {
  setActivities(state, {activities}) {
    state.list = activities[0].list;
  }
}

export const actions = {
  async fetchActivities({commit}) {
    const activities = await this.$axios.$get('/api/activities')
    commit('setActivities', {activities});
  }
}
