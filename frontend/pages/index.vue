<template>
  <div>
    <v-flex sm6>
      <RecentWidget />
    </v-flex>
  </div>
</template>

<script>
import RecentWidget from '~/components/RecentWidget.vue'

export default {
  components: {
    RecentWidget
  },
  head() {
    return {
      title: 'トップページ'
    }
  },
  async asyncData({ params, store }) {
    await store.dispatch('recent/fetchRecentStages');
    return {}
  }
}
</script>
