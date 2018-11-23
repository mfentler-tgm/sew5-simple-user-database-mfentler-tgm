<template>
    <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'User',
  data () {
    return {
      msg: ''
    }
  },
  methods: {
    getMessage () {
      axios.get('localhost:5000/user')
        .then((res) => {
          this.msg = res.data
        })
        .catch((error) => {
          this.msg = error
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
