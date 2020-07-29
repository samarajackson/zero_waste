<template>
  <div id="app">
    <Navbar/>
    <router-view></router-view>
  </div>
</template>

<script>
import Navbar from './components/Navbar'
export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.messages {
  color: crimson;
}

.pad {
  padding: 4%;
}

.nav-link:hover{
  color:#9f55ad !important;
}

.btn-info{
  background-color:#9f55ad;
  border-color:#9f55ad;
}

.btn-info:hover{
  background-color:#65376e;
}

#history{
  height:400px;
}
</style>
