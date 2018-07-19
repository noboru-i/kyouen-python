<template>
  <div class="green" :style="{width: width + 'px'}">
    <svg id="background-image" :width="width + 'px'" :height="width + 'px'">
      <line x1="0" :y1="(index + 0.5) * stoneSize" :x2="width" :y2="(index + 0.5) * stoneSize"
          :key="'row_' + index"
          stroke="#000"
          v-for="index in Array.from({length: 6}, (v, k) => k)"/>
      <line :x1="(index + 0.5) * stoneSize" y1="0" :x2="(index + 0.5) * stoneSize" :y2="width"
          :key="'col_' + index"
          stroke="#000"
          v-for="index in Array.from({length: 6}, (v, k) => k)"/>
    </svg>
    <v-btn fab
        color="blue-grey"
        :class="{hide: stone == '0', 'darken-3': stone == '1', 'lighten-5': stone == '2'}"
        v-for="(stone, index) in stageArray"
        :key="index"
        @click="$emit('on-stone-click', index)" />
  </div>
</template>

<script>
export default {
  props: ['stage', 'width'],
  computed: {
    boardSize: function() {
      return Math.sqrt(this.stage.length);
    },
    stoneSize: function() {
      return this.width / this.boardSize;
    },
    stageArray: function() {
      return this.stage.split('');
    }
  }
}
</script>

<style scoped>
#background-image {
  position: absolute;
}
.v-btn {
  margin: 0;
}
.v-btn.hide {
  opacity: 0;
}
</style>
