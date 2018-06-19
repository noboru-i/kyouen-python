<template>
  <div>
    <div>
      <h2>最新の登録</h2>
      <ul id="example-1">
        <li v-for="stage in stages" :key="stage.id">
          STAGE:{{ stage.stageNo }} - {{ stage.registDate }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState({
    stages: state => state.recent.list
  })
}
</script>
