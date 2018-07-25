import Vuex from 'vuex';
import { storiesOf } from '@storybook/vue'

import ActivityWidget from '../components/ActivityWidget.vue';

storiesOf('ActivityWidget', module)
  .add('normal', () => ({
    components: { ActivityWidget },
    template: `
      <div style="margin: 8px;">
        <ActivityWidget />
      </div>
    `,
    store: new Vuex.Store({
      state: {
        activity: {
          list: [{
            stageNo: 1,
            clearDate: '2018-06-22 09:34:19.613883'
          },{
            stageNo: 2,
            clearDate: '2018-06-23 09:34:19.613883'
          }]
        }
      }
    })
  }));

import RecentRegisteredStages from '../components/RecentRegisteredStages.vue';

storiesOf('RecentRegisteredStages', module)
  .add('normal', () => ({
    components: { RecentRegisteredStages },
    template: `
      <div style="margin: 8px;">
        <RecentRegisteredStages />
      </div>
    `,
    store: new Vuex.Store({
      state: {
        recentStages: [
          {
            creator: "creator 1",
            registerDate: "2018-07-19 23:44:08.676340",
            size: "6",
            stage: "100001010100000000111000001000010001",
            stageNo: "2622"
          },
          {
            creator: "creator 1",
            registerDate: "2018-07-19 23:42:54.894330",
            size: "6",
            stage: "100001010101000000011000000000010001",
            stageNo: "2621"
          },
        ]
      }
    })
  }));

import KyouenView from '../components/KyouenView.vue';

storiesOf('KyouenView', module)
  .add('normal', () => ({
    components: { KyouenView },
    template: `
      <KyouenView
          stage="000000010000001100001100000000001000"
          width="336" />
    `
  }));

import TumeKyouen from '../components/TumeKyouen.vue';

storiesOf('TumeKyouen', module)
  .add('normal', () => ({
    components: { TumeKyouen },
    template: `
      <TumeKyouen stage="000000010000001100001100000000001000" />
    `
  }));

import OverlayKyouenResult from '../components/OverlayKyouenResult.vue';
import { Point, Kyouen } from 'kyouen';

storiesOf('OverlayKyouenResult', module)
  .add('none', () => ({
    components: { OverlayKyouenResult },
    template: `
      <div style="background-color: #4caf50; width: 336px; height: 336px;">
        <OverlayKyouenResult
            boardSize="6"
            width="336"
            :kyouen-data="kyouenData"
            />
      </div>
    `,
    computed: {
      kyouenData () {
        return new Kyouen([
          new Point(0, 0),
          new Point(2, 3),
          new Point(3, 2),
          new Point(3, 3)]).hasKyouen();
      },
    }
  }))
  .add('circle', () => ({
    components: { OverlayKyouenResult },
    template: `
      <div style="background-color: #4caf50; width: 336px; height: 336px;">
        <OverlayKyouenResult
            boardSize="6"
            width="336"
            :kyouen-data="kyouenData"
            />
      </div>
    `,
    computed: {
      kyouenData () {
        return new Kyouen([
          new Point(2, 2),
          new Point(2, 3),
          new Point(3, 2),
          new Point(3, 3)]).hasKyouen();
      },
    }
  }))
  .add('line', () => ({
    components: { OverlayKyouenResult },
    template: `
      <div style="background-color: #4caf50; width: 336px; height: 336px;">
        <OverlayKyouenResult
            boardSize="6"
            width="336"
            :kyouen-data="kyouenData"
            />
      </div>
    `,
    computed: {
      kyouenData () {
        return new Kyouen([
          new Point(1, 0),
          new Point(2, 0),
          new Point(3, 0),
          new Point(4, 0)]).hasKyouen();
      },
    }
  }));
