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
            <div v-if="badges.length > 0" class="row">
              <div v-for ="badge in badges" class="col-sm badge" v-bind:key="badge.text">
                <img :src="badge.link" :alt="badge.text" width=50 class='m-2 badge'>
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
          <div class="col" v-if="check.length > 0">
            <Plotly :data="mydata" :layout="layout" :display-mode-bar="false" class="history"></Plotly>
          </div>
        </div>
    <div class="row text-center">
      <div class="col">
        <h4>My Recent Trashbags </h4>
        <b-table striped
          :items="trash"
          :fields="fields"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          :per-page="perPage"
          :current-page="currentPage"
          id="my_trash">
          <template v-slot:cell(type)="trash">
              <img :src="trash.item.type" width=25 height=25>
          </template>
          <template v-slot:cell(id)="trash">
            <b-link v-on:click="del(trash.item.id)"><img src="../../static/remove.png" width=25 height=25></b-link>
          </template>
        </b-table>
        <b-pagination
          v-model="currentPage"
          :total-rows="rows"
          :per-page="perPage"
          aria-controls="my-trash"
        ></b-pagination>
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
      badges: [],
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
      sortDesc: true,
      perPage: 5,
      currentPage: 1,
      check: []
    }
  },
  methods: {
    async getDashboardData () {
      await axios.get('mydashboard').then((response) => {
        const data = response.data
        // setting these values based on api response
        this.data = data.amounts
        this.user = data.user
        this.check = data.check
        // data modification functions, adding icons and necessary text
        this.percent = this.getPercentString(data.percent)
        this.trash = this.addTrashIcons(data.mytrash)
        this.badges = this.setupBadges(data.badges)
        this.checkForZeroWaste(parseInt(data.zerowasteweeks))
        // my data is for the plotly integration
        this.mydata = [{
          x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          y: data.amounts,
          type: 'bar',
          marker: {
            color: 'rgb(159, 85, 173)'
          }
        }]
      })
    },
    setupBadges (badges) {
      console.log('my badges: ' + badges)
      // loads in the badges icons based on what the user has won
      let badgeslinks = {
        '1': '../../static/first.png',
        '2': '../../static/second.png',
        '3': '../../static/third.png'
      }
      for (let i = 0; i < badges.length; i++) {
        badges[i].link = badgeslinks[badges[i].rank]
      }
      return badges
    },

    checkForZeroWaste (zerowasteweeks) {
      // adds a badge for the number of zero waste weeks
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
      // takes the current percent and generates the string to show on the front page
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
      // goes through my trash and maps the correct trash icon to show on dashboard
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

    async del (id) {
      await axios.delete('trashtest/' + id + '/').then((response) => {
        this.getDashboardData()
      })
    }
  },

  beforeMount () {
    if (this.$cookies.get('loggedin')) {
      this.getDashboardData()
    } else {
      this.$router.push({ path: '/' })
    }
  },

  computed: {
    rows () {
      // calculates the number of rows to show in pagination
      if (this.trash) {
        return this.trash.length
      } else {
        return null
      }
    }
  }
}
</script>
<style scoped>
.history{
  height: 400px;
}
.badge {
  display: inline;
}
</style>
