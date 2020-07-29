<template>
<div>
    <div class="jumbotron">
      <h1 class="display-4"> Welcome to Trash<img src="../../static/coldel.png" alt="Trash Icon" height=70 class="pb-2">Track </h1>
      <p class="lead">Track your waste production, compete with others, and earn achievements! View the top performing
        users below!</p>
    </div>
    <div class="Leaderboard row">
        <div class="table col">
        <Leaderboard v-bind:unit="{
          'api': 'monthlyleaderboard',
          'title': 'This Month\'s Leaderboard',
          'weight':'Waste Landfilled'
        }"/>
        </div>
        <div class="lbtable col">
        <Leaderboard v-bind:unit="{
          'api': 'annualleaderboard',
          'title': 'This Year\'s Leaderboard',
          'weight':'Average Waste/Month'
        }"/>
        </div>
    </div>
</div>
</template>
<script>
import Leaderboard from './Leaderboard.vue'
export default {
  components: {
    Leaderboard
  }
}
</script>
<style scoped>
    .lbtable {
        display: inline;
    }
</style>
