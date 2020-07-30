<template>
<div>
    <div class="jumbotron">
        <h1 class="display-4">Welcome to Trash<img src="../../static/coldel.png" alt="Trash Icon" height=70>Track, {{user}}! </h1>
        <p class="lead">{{percent}}</p> <p>The average American creates 134
            lb/month of waste. </p>
    </div>
    <div class="container">
        <div class="row text-center">
            <div class="col-sm">
            <h4 class="text-center">My Badges</h4>
            <div v-if="badges">
              <div v-for ="badge in badges" class="col-sm" v-bind:key="badge.text">
                <img :src="badge.link" :alt="badge.text" width=50 class='m-2'>
                <p>{{badge.text}}</p>
              </div>
            </div>
            <div v-else>
              <img src='../../static/sad.png' width=50 class='m-2'>
              <p>No badges, yet! Try to reduce your trash!</p>
            </div>
          </div>
        </div>
        <div class='row'>
          <div class="col" v-if="data">
            <Plotly :data="mydata" :layout="layout" :display-mode-bar="false" class="history"></Plotly>
          </div>
        </div>
    <div class="row text-center">
      <div class="col">
        <h4>My Recent Trashbags </h4>
        <b-table striped :items="trash" :fields="fields" :sort-by.sync="sortBy" :sort-desc.sync="sortDesc">
          <template v-slot:cell(type)="trash">
              <img :src="trash.item.type" width=25 height=25>
          </template>
          <template v-slot:cell(id)="trash">
            <b-button @click="delete(trash.item.id)"><img src="../../static/remove.png" width=25 height=25></b-button>
          </template>
        </b-table>
      </div>
    </div>
    </div>
</div>
</template>
<script>
import axios from 'axios'
import { Plotly } from 'vue-plotly'

export default {
  components: {
    Plotly
  },
  data () {
    return {
      user: {},
      badges: null,
      percent: 0,
      mydata: [],
      data: [],
      trash: null,
      zerowasteweeks: 0,
      fields: [{ key: 'date', label: 'Date' },
        { key: 'type', label: 'Trash Type' },
        { key: 'weight', label: 'Weight (lb)' },
        { key: 'size', label: 'Size (gal)' },
        { key: 'id', label: 'Delete' }],
      layout: {
        title: 'My Progress'
      },
      sortBy: 'date',
      sortDesc: true
    }
  },
  methods: {
    async getDashboardData () {
      await axios.create({ withCredentials: true }).get('mydashboard').then((response) => {
        const data = response.data
        this.data = data.amounts
        this.user = data.user
        this.badges = this.setupBadges(data.badges)
        this.percent = this.getPercentString(data.percent)
        this.checkForZeroWaste(parseInt(data.zerowasteweeks))
        this.trash = this.addTrashIcons(data.mytrash)
        this.mydata = [{
          x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          y: data.amounts,
          type: 'bar',
          marker: {
            color: 'rgb(159, 85, 173)'
          }
        }]
      }).catch(error => {
        if (error.status === 403 || error.status === 401) {
          this.$router.replace({ path: '/' })
        } else {
          console.log('some other error: ' + error.status)
        }
      })
    },
    setupBadges (badges) {
      let badgeslinks = {'1': '../../static/first.png',
        '2':'../../static/second.png',
        '3':'../../static/third.png'}
      for (let i=0; i<badges.length; i++){
        badges[i].link = badgeslinks[badges[i].place]
      }
      return badges
    },
    checkForZeroWaste (zerowasteweeks) {
      if (zerowasteweeks > 0) {
          let text = ''
          if (zerowasteweeks === 1) {
            text = zerowasteweeks + ' Zero Waste Week!'
          } else if (zerowasteweeks > 1) {
            text = zerowasteweeks + ' Zero Waste Weeks!'
          }
          this.badges.push({ text: text, link: '../../static/reward.png' })
        }
    },
    getPercentString (percent) {
      if (parseFloat(percent) === 0 || percent === undefined) {
          return 'Start tracking your waste to see how you compare to the average American!'
        } else if (parseFloat(percent) < 0) {
          percent = percent * -1
          return 'You create ' + percent + '% more trash than the average American.'
        } else {
          return 'You create ' + percent + '% less trash than the average American.'
        }
    },
    addTrashIcons (mytrash) {
      if (mytrash) {
        for (let i = 0; i < mytrash.length; i++) {
          const trash = mytrash[i]
          if (parseFloat(trash.weight) > 0) {
            trash.type = '../../static/trash.png'
          } else {
            trash.type = '../../static/reward.png'
          }
        }
        return mytrash
      }
    },
    async delete (id) {
      await axios.create({withCredentials: true}).delete('trashtest', id).then((response) => {
        this.getDashboardData()
      })
    }
  },
  beforeMount () {
    this.getDashboardData()
  }
}
</script>
<style scoped>
.history{
  height:400px;
}
</style>
