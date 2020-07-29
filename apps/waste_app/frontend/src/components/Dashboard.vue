<template>
<div>
    <div class="jumbotron">
        <h1 class="display-4">Welcome to Trash<img src="../../static/coldel.png" alt="Trash Icon" height=70>Track, {{user}}
            ! </h1>
        <p class="lead">{{percent}}</p> <p>The average American creates 134
            lb/month of waste. </p>
    </div>
    <div class="container">
        <div class="row text-center">
            <div class="col-sm">
            <h4 class="text-center">My Badges</h4>
          </div>
        </div>
        <div class='row'>
          <div class="col">
            <Plotly :data="mydata" :layout="layout" :display-mode-bar="false" class="history"></Plotly>
          </div>
        </div>
        <!-- <div class="row" v-for="item in badges.items" :key="item" >
            {% for key, item in badges.items %}
            <div class="col-sm">
                {{item.link}}
                <p>{{item.desc}}</p>
            </div>
        </div> -->
    <div class="row text-center">
      <h4>My Recent Trashbags </h4>
      <b-table striped :items="trash" :fields="fields">
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
      badges: {},
      percent: 0,
      mydata: [],
      trash: null,
      zerowasteweeks: 0,
      fields: [{ key: 'date', label: 'Date' },
        { key: 'type', label: 'Trash Type' },
        { key: 'weight', label: 'Weight (lb)' },
        { key: 'size', label: 'Size (gal)' },
        { key: 'id', label: 'Delete' }],
      layout: {
        title: 'My Progress'
      }
    }
  },
  methods: {
    async getDashboardData () {
      await axios.create({ withCredentials: true }).get('mydashboard').then((response) => {
        const data = response.data
        this.badges = data.badges
        let percent = data.percent
        this.mydata = [{
          x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          y: data.amounts,
          type: 'bar',
          marker: {
            color: 'rgb(159, 85, 173)'
          }
        }]
        console.log(this.mydata)
        this.user = data.user
        let text = ''
        if (parseFloat(percent) === 0) {
          this.percent = 'Start tracking your waste to see how you compare to the average American!'
        } else if (parseFloat(percent) < 0) {
          percent = percent * -1
          this.percent = 'You create ' + percent + '% more trash than the average American.'
        } else {
          this.percent = 'You create ' + percent + '% less trash than the average American.'
        }
        if (data.zerowasteweeks > 0) {
          if (parseInt(data.zerowasteweeks) === 1) {
            text = data.zerowasteweeks + ' Zero Waste Week!'
          } else if (parseInt(data.zerowasteweeks) > 1) {
            text = data.zerowasteweeks + ' Zero Waste Weeks!'
          }
          this.badges.push({ desc: text, link: '../../static/reward.png' })
        }
        for (let i = 0; i < data.mytrash.length; i++) {
          const trash = data.mytrash[i]
          if (parseFloat(trash.weight) > 0) {
            trash.type = '../../static/trash.png'
          } else {
            trash.type = '../../static/reward.png'
          }
        }
        this.trash = data.mytrash
      })
    },
    async delete (id) {
      await axios.create({ withCredentials: true }).delete('trashtest', id).then((response) => {
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
