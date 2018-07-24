<template>
  <div class="green" :style="{width: width + 'px', height: width + 'px'}">
    <svg id="background-image" :width="width + 'px'" :height="width + 'px'">
      <line x1="0" :y1="(index + 0.5) * stoneSize" :x2="width" :y2="(index + 0.5) * stoneSize"
          :key="'row_' + index"
          stroke="#000"
          v-for="index in Array.from({length: 6}, (v, k) => k)"/>
      <line :x1="(index + 0.5) * stoneSize" y1="0" :x2="(index + 0.5) * stoneSize" :y2="width"
          :key="'col_' + index"
          stroke="#000"
          v-for="index in Array.from({length: 6}, (v, k) => k)"/>
      <line
          :x1="computedLine.startX" :y1="computedLine.startY"
          :x2="computedLine.stopX" :y2="computedLine.stopY"
          stroke="#fff"
          stroke-width="3"
          v-if="kyouenData.lineKyouen === true"
          />
      <circle :cx="computedCenter.x" :cy="computedCenter.y" :r="computedRadius"
          stroke="#fff"
          stroke-width="3"
          fill="#fff"
          fill-opacity="0.1"
          v-else="kyouenData.lineKyouen ==== true"
          />
    </svg>
  </div>
</template>

<script>
export default {
  props: ['boardSize', 'width', 'kyouenData'],
  computed: {
    stoneSize: function() {
      return this.width / this.boardSize;
    },
    computedCenter: function() {
      let offset = this.stoneSize * 0.5;
      return {
        x: this.kyouenData.center.x * this.stoneSize + offset,
        y: this.kyouenData.center.y * this.stoneSize + offset
      };
    },
    computedRadius: function() {
      return this.kyouenData.radius * this.stoneSize;
    },
    computedLine: function() {
      let offset = this.stoneSize * 0.5;
      const line = this.kyouenData.line;
      console.log(this.kyouenData);
      if (line.a === 0) {
        return {
          startX: 0,
          startY: line.getY(0) * this.stoneSize + offset,
          stopX: this.width,
          stopY: line.getY(0) * this.stoneSize + offset
        };
      } else if (line.b === 0) {
        return {
          startX: line.getX(0) * this.stoneSize + offset,
          startY: 0,
          stopX: line.getX(0) * this.stoneSize + offset,
          stopY: this.width
        };
      } else {
        if (-1 * line.c / line.b > 0) {
          return {
            startX: 0,
            startY: line.getY(-0.5) * this.stoneSize + offset,
            stopX: this.width,
            stopY: line.getY(this.boardSize - 0.5) * this.stoneSize + offset
          };
        } else {
          return {
            startX: line.getX(-0.5) * this.stoneSize + offset,
            startY: 0,
            stopX: line.getX(this.boardSize - 0.5) * this.stoneSize + offset,
            stopY: this.width
          };
        }
      }
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
