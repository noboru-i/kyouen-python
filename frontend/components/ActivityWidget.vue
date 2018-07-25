<template>
  <v-card>
    <v-card-title primary-title>
      <div>
        <h3 class="headline mb-2">アクティビティ</h3>
        <ul>
          <li v-for="activity in activities" :key="activity.stageNo">
            STAGE:{{ activity.stageNo }} - {{ activity.clearDate }}
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
    activities: state => state.activity.list
  })
}
</script>

<style scoped>
ul {
  list-style-type: none;
}
</style>
