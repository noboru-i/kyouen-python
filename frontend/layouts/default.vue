<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      width="180"
      app
    >
      <AppNavigation />
    </v-navigation-drawer>
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title>共円</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn flat>ログイン</v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout>
          <v-flex>
            <nuxt />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <v-footer color="indigo" app>
      <v-flex xs12 py-3 text-xs-center white--text>
        &copy; 2018 <strong>noboru</strong>
      </v-flex>
    </v-footer>
  </v-app>
</template>

<script>
import AppNavigation from '~/components/AppNavigation.vue'

export default {
  components: {
    AppNavigation
  },
  data: () => ({
    drawer: null
  }),

  props: {
    source: String
  }
}
</script>
