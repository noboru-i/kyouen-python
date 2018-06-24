<template>
  <div class="green background">
    <svg id="background-image" width="336px" height="336px">
      <line x1="0" :y1="(index + 0.5) * stoneSize" :x2="width" :y2="(index + 0.5) * stoneSize"
          stroke="#000"
          v-for="index in Array.from({length: 6}, (v, k) => k)"/>
      <line :x1="(index + 0.5) * stoneSize" y1="0" :x2="(index + 0.5) * stoneSize" :y2="width"
          stroke="#000"
          v-for="index in Array.from({length: 6}, (v, k) => k)"/>
    </svg>
    <v-btn fab
        color="blue-grey darken-3"
        :class="{hide: stone == '0'}"
        v-for="(stone, index) in stageArray"
        :key="index" />
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data: function() {
    return {
      width: 336
    }
  },
  props: ['stage'],
  computed: {
    stoneSize: function() {
      return this.width / 6;
    },
    stageArray: function() {
      return this.stage.split('');
    }
  }
}
</script>

<style lang="postcss" scoped>
.background {
  width: 336px;
}
#background-image {
  position: absolute;
}
.btn {
  margin: 0;
}
.btn.hide {
  opacity: 0;
}
</style>
