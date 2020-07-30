<template>
<div class="container pt-3">
    <h1>Register for TrashTrack</h1>
    <b-form @submit.prevent="register">
        <input type="hidden" name="_token" :value="csrf">
        <b-form-group id="first-group"
            label="First Name"
            label-for="first"
        >
        <b-form-input
            id ="first"
            v-model="user.first_name"
            type="text"
        ></b-form-input>
        <b-form-text v-if="errors.first_name" force-show=true class="error">
            erorrrrr
            <div v-for="error in errors.first_name" :key="error">
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
            v-model="user.last_name"
            type="text"
        ></b-form-input>
        <b-form-text  v-if="errors.last_name">
            <div v-for="error in errors.last_name" :key="error">
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
            v-model="user.password"
            type="password"
        ></b-form-input>
         <b-form-text  v-if="errors.password">
            <div v-for="error in errors.password" :key="error">
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
        <b-button type="submit" class='btn btn-info'>Submit</b-button>
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
        console.log('then executed:')
        this.$router.replace({ path: './../dashboard' })
      }).catch(error => {
        console.log('got an error:' + error)
        this.errors = error.response.data
      })
    }
  }
}
</script>
<style scoped>

</style>
