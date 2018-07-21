import Vuex from 'vuex';
import { storiesOf } from '@storybook/vue'

import ActivityWidget from '../components/ActivityWidget.vue'

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
          }]
        }
      }
    })
  }));

import KyouenView from '../components/KyouenView.vue'

storiesOf('KyouenView', module)
  .add('normal', () => ({
    components: { KyouenView },
    template: `
      <KyouenView
          stage="000000010000001100001100000000001000"
          width="336" />
    `
  }));

import TumeKyouen from '../components/TumeKyouen.vue'

storiesOf('TumeKyouen', module)
  .add('normal', () => ({
    components: { TumeKyouen },
    template: `
      <TumeKyouen stage="000000010000001100001100000000001000" />
    `
  }));
