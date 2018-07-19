<template>
  <div>
    <KyouenView
        :stage="kyouen.stage"
        :width="width"
        @on-stone-click="onStoneClick" />
    <v-btn
        color="primary"
        @click="onClick()"
        :style="{width: width + 'px'}">共円！</v-btn>
  </div>
</template>

<script>
import { Kyouen, Point } from 'kyouen'

import KyouenView from './KyouenView'

String.prototype.replaceCharAt = function(at, replaceChar) {
  const before = this.substring(0, at);
  const after = this.slice(at + 1);
  return before + replaceChar + after;
};

class TumeKyouenState {
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
      kyouen: new TumeKyouenState(this.stage)
    }
  },
  props: ['stage'],
  components: {
    KyouenView
  },
    computed: {
    boardSize: function() {
      return Math.sqrt(this.stage.length);
    },
    stoneSize: function() {
      return this.width / this.boardSize;
    },
    stageArray: function() {
      return this.kyouen.stage.split('');
    }
  },
  methods: {
    onStoneClick: function(index) {
      this.kyouen.selecWithIndext(index);
    },
    onClick: function() {
      const whiteCount = this.stageArray.reduce((accumulator, currentValue) => {
        return accumulator + (currentValue === "2" ? 1 : 0)
      }, 0);
      if (whiteCount !== 4) {
        return;
      }
      var stones = [];
      this.stageArray.forEach((val, index) => {
        if (val === '2') {
          const x = index % this.boardSize;
          const y = Math.floor(index / this.boardSize);
          stones.push(new Point(x, y));
        }
      });

      console.log(new Kyouen(stones).hasKyouen());
    }
  }
}
</script>

<style scoped>
.v-btn {
  margin: 0;
}
.v-btn.hide {
  opacity: 0;
}
</style>
