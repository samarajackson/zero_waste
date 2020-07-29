<template>
<div>
    <div class="jumbotron">
        <h1 class="display-4">Take out the Trash</h1>
        <img src="../../static/coldel.png" alt="Trash Icon" height=80 class="pb-2">
        <p class="lead">Fill out the fields below, or select "Zero Waste" to record your week as trash-free!</p>
        <div class="col-lg align-self-center">
            <a href="../zero_waste" class="btn btn-success">Zero Waste Week!</a>
        </div>
    </div>
    <div class="container pt-3">
        <h1></h1>
        <b-form @submit="trash">
            <!-- <input type="hidden" name="_token" :value="csrf"> -->
            <b-form-group id="bag_size-group"
                label="How big is your bag?"
                label-for="bag_size"
            >
            <b-form-select
                id ="bag_size"
                v-model="trashtest.bag_size"
                :options="bagOptions"
            ></b-form-select>
            <b-form-text v-if="errors.bag_size" force-show=true class="text-danger">
                <div v-for="error in errors.bag_size" :key="error">
                    {{error}}
                </div>
            </b-form-text>
            </b-form-group>
             <b-form-group id="fullness-group"
                label="How full is your bag?"
                label-for="fullness"
            >
            <b-form-select
                id ="fullness"
                v-model="trashtest.fullness"
                :options="fullness"
            ></b-form-select>
            <b-form-text v-if="errors.fullness" force-show=true class="text-danger">
                <div v-for="error in errors.fullness" :key="error">
                    {{error}}
                </div>
            </b-form-text>
            </b-form-group>
            <b-form-group id="takeout_date-group"
                label="When did you throw it out?"
                label-for="takeout_date"
            >
            <b-form-input
                id ="takeout_date"
                v-model="trashtest.takeout_date"
                type="date"
                :value = now
            ></b-form-input>
            <b-form-text  v-if="errors.takeout_date">
                <div v-for="error in errors.bday" :key="error">
                    {{error}}
                </div>
            </b-form-text >
            </b-form-group>
            <b-button type="submit">Submit</b-button>
        </b-form>
    </div>
</div>
</template>
<script>
import axios from 'axios'
export default {
  data () {
    return {
      user: {},
      csrf: '',
      errors: {},
      trashtest: {},
      bagOptions: [
        { value: 4, text: 'Small (4gal)' },
        { value: 13, text: 'Tall Kitchen (13gal)', selected: true },
        { value: 30, text: 'Large Trash (30gal)' }
      ],
      fullness: [
        { value: 1, text: 'Full' },
        { value: 0.75, text: 'Mostly Full' },
        { value: 0.5, text: 'Half Full' },
        { value: 0.25, text: 'Mostly Empty' }
      ],
      weightdict: {
        4: 4,
        13: 15,
        30: 25
      },
      now: ''
    }
  },
  methods: {
    async trash () {
      this.trashtest.weight = this.trashtest.fullness * (this.weightdict[this.trashtest.bag_size])
      this.trashtest.trashtype = 'Trashbag'
      axios.create({ withCredentials: true }).post('trashtest/', this.trashtest).then((response) => {
        this.$router.replace({ path: './../dashboard' })
      })
        .catch(error => {
          this.errors = error.response.data
        })
    }
  },
  mounted () {
    this.csrf = window.laravel.csrfToken
    const today = new Date()
    const dd = String(today.getDate()).padStart(2, '0')
    const mm = String(today.getMonth() + 1).padStart(2, '0')
    const yyyy = today.getFullYear()
    this.now = mm + '-' + dd + '-' + yyyy
    console.log('date is ' + this.now)
  }
}
</script>
