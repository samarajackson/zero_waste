<template>
<div class="container pt-3">
    <h1>Register for TrashTrack</h1>
    <b-form @submit="register">
        <input type="hidden" name="_token" :value="csrf">
        <b-form-group id="first-group"
            label="First Name"
            label-for="first"
        >
        <b-form-input
            id ="first"
            v-model="user.first"
            type="text"
        ></b-form-input>
        <b-form-text v-if="errors.first" force-show=true class="text-danger">
            <div v-for="error in errors.first" :key="error">
                {{error}}
            </div>
        </b-form-text>
        </b-form-group>
        <b-form-group id="last-group"
            label="Last Name"
            label-for="last"
        >
        <b-form-input
            id ="last"
            v-model="user.last"
            type="text"
        ></b-form-input>
        <b-form-text  v-if="errors.last">
            <div v-for="error in errors.last" :key="error">
                {{error}}
            </div>
        </b-form-text >
        </b-form-group>
        <b-form-group id="email-group"
            label="Email Address"
            label-for="email"
        >
        <b-form-input
            id ="email"
            v-model="user.email"
            type="email"
        ></b-form-input>
        <b-form-text  v-if="errors.email">
            <div v-for="error in errors.email" :key="error">
                {{error}}
            </div>
        </b-form-text >
        </b-form-group>
        <b-form-group id="username-group"
            label="Public Username"
            label-for="username"
        >
        <b-form-input
            id ="username"
            v-model="user.username"
            type="text"
        ></b-form-input>
         <b-form-text  v-if="errors.username">
            <div v-for="error in errors.username" :key="error">
                {{error}}
            </div>
        </b-form-text >
        </b-form-group>
        <b-form-group id="bday-group"
            label="Birthday"
            label-for="bday"
        >
        <b-form-input
            id ="bday"
            v-model="user.bday"
            type="date"
        ></b-form-input>
         <b-form-text  v-if="errors.bday">
            <div v-for="error in errors.bday" :key="error">
                {{error}}
            </div>
        </b-form-text >
        </b-form-group>
        <b-form-group id="pw-group"
            label="Password"
            label-for="pw"
        >
        <b-form-input
            id ="pw"
            v-model="user.pw"
            type="password"
        ></b-form-input>
         <b-form-text  v-if="errors.pw">
            <div v-for="error in errors.pw" :key="error">
                {{error}}
            </div>
        </b-form-text >
        </b-form-group>
        <b-form-group id="pw2-group"
            label="Confirm Password"
            label-for="pw2"
        >
        <b-form-input
            id ="pw2"
            v-model="user.pw2"
            type="password"
        ></b-form-input>
        </b-form-group>
        <b-button type="submit">Submit</b-button>
    </b-form>
</div>
</template>
<script>
import axios from 'axios'
export default {
  data () {
    return {
      user: {},
      csrf: '',
      errors: {}
    }
  },
  methods: {
    async register (data) {
      this.errors = {}
      axios.post('user/', this.user).then((response) => {
        this.$router.replace({ path: './../dashboard' })
      })
        .catch(error => {
          this.errors = error.response.data
        })
    }
  },
  mounted () {
    this.csrf = window.laravel.csrfToken
  }
}
</script>
