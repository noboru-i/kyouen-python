<template>
  <div class="green background">
    <svg id="background-image" width="336px" height="336px">
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
        @click="onClick(index)" />
  </div>
</template>

<script>
import { mapState } from 'vuex'

const boardSize = 6;

String.prototype.replaceCharAt = function(at, replaceChar) {
  const before = this.substring(0, at);
  const after = this.slice(at + 1);
  return before + replaceChar + after;
};

class TumeKyouen {
  constructor(stage) {
    this.stage = stage;
  }

  selecWithIndext(index) {
    const c = this.stage.charAt(index);
    this.stage = this.stage.replaceCharAt(index, this.getNextChar(c));
  }

  getNextChar(char) {
    if (char === '1') {
      return '2';
    } else if (char === '2') {
      return '1';
    }
    return char;
  }
}

export default {
  data: function() {
    return {
      width: 336,
      kyouen: new TumeKyouen(this.stage)
    }
  },
  props: ['stage'],
  computed: {
    stoneSize: function() {
      return this.width / boardSize;
    },
    stageArray: function() {
      return this.kyouen.stage.split('');
    }
  },
  methods: {
    onClick: function (index) {
      this.kyouen.selecWithIndext(index);
    }
  }
}
</script>

<style scoped>
.background {
  width: 336px;
}
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
