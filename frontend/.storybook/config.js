import "vuetify/dist/vuetify.css";

import { configure, addDecorator } from "@storybook/vue"
import Vue from "vue";
import Vuex from 'vuex';
import Vuetify from "vuetify";

Vue.use(Vuex);
Vue.use(Vuetify);

const VAppDecorator = (story) => ({
  components: { Story: story() },
  template: `
    <v-app>
      <story />
    </v-app>
  `
});
addDecorator(VAppDecorator);

const loadStories = () => {
  require("../stories/index")
}

configure(loadStories, module)
