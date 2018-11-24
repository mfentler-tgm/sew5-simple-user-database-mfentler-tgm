<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-9">
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Picture</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in results" :key="index">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span v-if="user.picture">{{user.picture}}</span>
                <span v-else>&nsbp</span>
              </td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'User',
  data () {
    return {
      results: null
    }
  },
  methods: {
    getMessage () {
      const path = 'http://localhost:5000/user'
      axios.get(path)
        .then((res) => {
          this.results = res.data
        })
        .catch((error) => {
          this.results = error
        })
    }
  },
  created () {
    this.getMessage()
  }
}
</script>

<style scoped>

</style>
