<template>
  <v-container grid-list-md>
    <div class="text-xs-center">
      <v-pagination
        :length="6"
        circle
        v-model="page">
      </v-pagination>
      {{ stages }}
    </div>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState({
    stages: state => state.stages.list
  }),
  data () {
    return {
      page: 1
    }
  },
  head() {
    return {
      title: 'ステージ一覧'
    }
  },
  async asyncData({ params, store }) {
    store.dispatch('stages/fetchListStages', { page : 1 })
    return {}
  }
}
</script>
