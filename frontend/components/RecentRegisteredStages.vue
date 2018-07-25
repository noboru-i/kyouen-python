<template>
  <v-card>
    <v-card-title primary-title>
      <v-layout>
        <v-flex xs12>
      <div>
        <div class="headline">最新の登録</div>
        <div>
          <ul>
            <li v-for="recentStage in recentStages" :key="recentStage.stageNo" class="mt-2">
              <v-card class="inner_card">
                <div class="stage_no">STAGE:{{ recentStage.stageNo }}</div>
                <div class="created_by">created by {{ recentStage.creator }}</div>
                <div class="register_date">{{ recentStage.registerDate }}</div>
              </v-card>
            </li>
          </ul>
        </div>
      </div>
        </v-flex>
      </v-layout>
    </v-card-title>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState({
    recentStages: state => state.recentStages
  })
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding-left: 0;
}

.inner_card {
  padding: 8px;
}
.created_by {
  text-align: right;
}
.register_date {
  text-align: right;
}
</style>
