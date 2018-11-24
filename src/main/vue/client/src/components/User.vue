<template>
    <div>
    <p>{{ results }}</p>
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
      axios({
        method: 'get',
        url: 'http://localhost:5000/user',
        timeout: 60 * 0.5 * 1000
      })
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
