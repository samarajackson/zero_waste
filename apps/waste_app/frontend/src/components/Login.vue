<template>
<div>
    <div class="jumbotron">
        <h1 class="display-4">Welcome to Trash<img src="../../static/coldel.png" alt="Trash Icon" height=70 class="pb-2">Track</h1>
        <p class="lead">Track your waste production, compete with others, and earn achievements! Please log in below.</p>
    </div>
    <div class="container">
    <b-form @submit.prevent="login">
        <!-- <input type="hidden" name="_token" :value="csrf"> -->
        <b-form-group id="email-group"
            label="Email address"
            label-for="email"
        >
        <b-form-input
            id ="email"
            v-model="user.email"
            type="email"
            placeholder="Enter email"
        ></b-form-input>
        <b-form-text v-if="errors.email">
          {{errors.email}}
        </b-form-text>
        </b-form-group>
        <b-form-group id="pw-group"
            label="Password"
            label-for="pw"
        >
        <b-form-input
            id ="pw"
            v-model="user.password"
            type="password"
        ></b-form-input>
        <b-form-text v-if="errors.password" force-show=true class="text-danger">
            {{errors.password}}
        </b-form-text>
        </b-form-group>
        <b-button type="submit" class='btn btn-info' size="lg">Login</b-button>
    </b-form>
    <div class="pt-4">
        <h4>Don't have an account? No problem!</h4>
        <b-button router-link to="/register" size="lg">Register</b-button>
    </div>
    </div>
</div>
</template>
<script>
import axios from 'axios'

export default {
  data () {
    return {
      user: {},
      errors: {}
    }
  },
  methods: {
    async login () {
      await axios.post('login', this.user).then((response) => {
        this.errors = {}
        if (response.data.errors) {
          this.errors = response.data.errors
        } else {
          this.$store.commit('changeid', response.data.id)
          this.$cookies.set('loggedin', true)
          this.$router.push({ path: 'dashboard' })
        }
      })
    }
  }
}
</script>
