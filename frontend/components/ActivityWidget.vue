<template>
  <v-card>
    <v-card-title primary-title>
      <div>
        <h3 class="headline mb-2">アクティビティ</h3>
        <ul id="example-1">
          <li v-for="stage in stages" :key="stage.id">
            STAGE:{{ stage.stageNo }} - {{ stage.registDate }}
          </li>
        </ul>
      </div>
    </v-card-title>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState({
    stages: state => state.recent.list
  })
}
</script>

<style lang="postcss" scoped>
ul {
  list-style-type: none;
}
</style>
