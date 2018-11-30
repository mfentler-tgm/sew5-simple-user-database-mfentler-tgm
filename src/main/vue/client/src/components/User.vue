<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>User</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.user-modal>Add User</button>
        <br><br>

        <!-- books table -->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Picture</th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.picture }}</td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.user-update-modal
                        @click="editUser(user)">
                    Update
                </button>
              </td>
              <td>
                <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteUser(user)">
                    Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>

    <!-- add book modal -->
    <b-modal ref="addUserModal"
             id="user-modal"
            title="Add a new user"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-username-group"
                      label="Username:"
                      label-for="form-username-input">
            <b-form-input id="form-username-input"
                          type="text"
                          v-model="addUserForm.username"
                          required
                          placeholder="Enter username">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-email-group"
                      label="Email:"
                      label-for="form-email-input">
          <b-form-input id="form-email-input"
                        type="email"
                        v-model="addUserForm.email"
                        required
                        placeholder="Enter email">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-picture-group"
                      label="Picture:"
                      label-for="form-picture-input">
          <b-form-input id="form-picture-input"
                        type="text"
                        v-model="addUserForm.picture"
                        required
                        placeholder="Enter picture link">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="editUserModal"
             id="user-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-username-edit-group"
                      label="Username:"
                      label-for="form-username-edit-input">
          <b-form-input id="form-username-edit-input"
                        type="text"
                        v-model="editForm.username"
                        required
                        placeholder="Enter username">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-email-edit-group"
                      label="Email:"
                      label-for="form-email-edit-input">
          <b-form-input id="form-email-edit-input"
                        type="email"
                        v-model="editForm.email"
                        required
                        placeholder="Enter Email">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-picture-edit-group"
                      label="Picture:"
                      label-for="form-picture-edit-input">
          <b-form-input id="form-picture-edit-input"
                        type="text"
                        v-model="editForm.picture"
                        required
                        placeholder="Picture">
          </b-form-input>
        </b-form-group>
        <b-button id="edit-form-submit-button" type="submit" variant="primary">Update</b-button>
        <b-button id="edit-form-cancel-button" type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      users: [],
      addUserForm: {
        username: '',
        email: '',
        picture: ''
      },
      editForm: {
        id: '',
        username: '',
        email: '',
        picture: ''
      },
      message: '',
      showMessage: false
    }
  },
  methods: {
    getUser () {
      const path = 'http://localhost:5000/user'
      axios.get(path)
        .then((res) => {
          this.users = res.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    addUser (payload) {
      const path = 'http://localhost:5000/user'
      axios.post(path, payload)
        .then(() => {
          this.getUser()
          this.message = 'User added!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getUser()
        })
    },
    updateUser (payload, userID) {
      const path = `http://localhost:5000/user/${userID}`
      axios.put(path, payload)
        .then(() => {
          this.getUser()
          this.message = 'User updated!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getUser()
        })
    },
    removeUser (userID) {
      const path = `http://localhost:5000/user/${userID}`
      axios.delete(path)
        .then(() => {
          this.getUser()
          this.message = 'User removed!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getUser()
        })
    },
    initForm () {
      this.addUserForm.username = ''
      this.addUserForm.email = ''
      this.addUserForm.picture = ''
      this.editForm.id = ''
      this.editForm.username = ''
      this.editForm.email = ''
      this.editForm.picture = ''
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addUserModal.hide()
      const payload = {
        username: this.addUserForm.username,
        email: this.addUserForm.email,
        picture: this.addUserForm.picture
      }
      this.addUser(payload)
      this.initForm()
    },
    onSubmitUpdate (evt) {
      evt.preventDefault()
      this.$refs.editUserModal.hide()
      const payload = {
        username: this.editForm.username,
        email: this.editForm.email,
        picture: this.editForm.picture
      }
      this.updateUser(payload, this.editForm.id)
    },
    onReset (evt) {
      evt.preventDefault()
      this.$refs.addUserModal.hide()
      this.initForm()
    },
    onResetUpdate (evt) {
      evt.preventDefault()
      this.$refs.editUserModal.hide()
      this.initForm()
      this.getUser() // why?
    },
    onDeleteUser (user) {
      this.removeUser(user.id)
    },
    editUser (user) {
      this.editForm = user
    }
  },
  created () {
    this.getUser()
  }
}
</script>
