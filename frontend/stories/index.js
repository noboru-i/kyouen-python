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

import Kyouen from '../components/Kyouen.vue'

storiesOf('Kyouen', module)
  .add('normal', () => ({
    components: { Kyouen },
    template: `
      <Kyouen stage="100000110000000000000000000000000001" />
    `
  }));
