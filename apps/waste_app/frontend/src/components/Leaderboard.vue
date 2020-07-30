<template>
    <div>
        <h4>{{unit.title}}</h4>
        <b-table striped :items="rankingsdata" :fields="fields">
            <template v-slot:cell(rank)="rankingsdata">
                <div v-if="(rankingsdata.item.rank).length > 3"> <img :src="rankingsdata.item.rank" width=25 height=25></div>
                <div v-else>{{rankingsdata.item.rank}} </div>
            </template>
        </b-table>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      rankingsdata: null,
      fields: [{ key: 'rank' }, { key: 'user__username', label: 'Username' }, { key: 'weight__sum', label: this.unit.weight }]
    }
  },
  props: ['unit'],
  methods: {
    async getRankingsData () {
      await axios.get(this.unit.api).then((response) => {
        const data = response.data
        // Adding special icons to first through third place
        const rankinglinks = ['../../static/first.png', '../../static/second.png', '../../static/third.png']
        for (let i = 0; i < data.length; i++) {
          if (i <= 2) {
            data[i].rank = rankinglinks[i]
          } else {
            data[i].rank = i + 1
          }
        }
        this.rankingsdata = data
      })
    }
  },
  created () {
    this.getRankingsData()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
