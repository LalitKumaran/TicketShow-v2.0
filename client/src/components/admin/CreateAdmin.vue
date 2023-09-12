<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Create Admin</h3>
        <form @submit.prevent="register">
          <input
            name="username"
            placeholder="Username"
            type="text"
            v-model="username"
            required
          />
          <input
            name="email"
            placeholder="Email"
            type="email"
            v-model="email"
            required
          />
          <input
            name="password"
            placeholder="Password"
            type="password"
            v-model="password"
            required
          />
          <input
            placeholder="Mobile Number"
            type="tel"
            v-model="mobile"
            required
          />
          <input
            placeholder="Location"
            type="text"
            v-model="location"
            required
          />
          <button class="btn btn-outline-warning" type="submit">
            Register
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import axios from "axios";
export default {
  name: "create-admin",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      mobile: "",
      location: "",
    };
  },
  components: {
    Navbar,
  },
  methods: {
    register() {
      axios
        .post("", {
          username: this.username,
          email: this.email,
          password: this.password,
          mobile: this.mobile,
          location: this.location,
          role: "admin",
        })
        .then((res) => {
          setTimeout(() => {
            this.$router.push("/venues");
          }, 2000);
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
<style></style>
