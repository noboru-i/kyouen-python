<template>
  <div>
    <h1>共円</h1>
    <div>
      <h2>最新の登録</h2>
      <ul id="example-1">
        <li v-for="stage in stages" :key="stage.id">
          STAGE:{{ stage.stageNo }} - {{ stage.registDate }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  async asyncData({ params, app}) {
    const stages = await app.$axios.$get(location.href + 'api/recent_stages')

    return {stages}
  }
}
</script>
