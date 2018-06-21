<template>
  <v-container grid-list-md>
    <v-layout row wrap>
      <v-flex xs12 sm6>
        <RecentWidget />
      </v-flex>
      <v-flex xs12 sm6>
        <ActivityWidget />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import RecentWidget from '~/components/RecentWidget.vue'
import ActivityWidget from '~/components/ActivityWidget.vue'

export default {
  components: {
    RecentWidget,
    ActivityWidget
  },
  head() {
    return {
      title: 'トップページ'
    }
  },
  async asyncData({ params, store }) {
    await Promise.all([
      store.dispatch('recent/fetchRecentStages'),
      store.dispatch('activity/fetchActivities')
    ]);
    return {}
  }
}
</script>
