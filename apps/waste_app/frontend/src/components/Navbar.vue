<template>
<header>
  <b-navbar class="navbar navbar-expand-lg navbar-light bg-light">
    <b-navbar-brand href="/">
      Trash
      <img src="../../static/coldel.png" width="25" height="25" class="d-inline-block align-top" alt="TrashTrack"/>Track
    </b-navbar-brand>
    <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
            <div v-if="$store.state.userid==null" class="row">
              <b-nav-item><router-link to="/" class='nav-link'>Leaderboard</router-link></b-nav-item>
              <b-nav-item><router-link to="/login" class='nav-link'>Login</router-link></b-nav-item>
            </div>
            <div v-else class="row">
                <b-nav-item><router-link to="/takeout" class='nav-link'>Take out the Trash</router-link></b-nav-item>
                <b-nav-item><router-link to='/dashboard' class='nav-link'>My Dashboard</router-link></b-nav-item>
                <b-nav-item><a @click="logout" class='nav-link'>Logout</a></b-nav-item>
            </div>
        </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</header>
</template>

<script>
export default {
  methods: {
    logout () {
      this.$store.commit('changeid', null)
      this.$store.commit('updateuser', null)
      this.$cookies.remove('userid')
      this.$router.replace({path: '/'})
    }
  }
}
</script>
