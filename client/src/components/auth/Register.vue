<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Register</h3>
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
            type="password"
            placeholder="Password"
            autocomplete="on"
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
          <p class="text-warning">
            Already have an account?
            <router-link class="text-warning" to="/">Login</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import BootstrapToast from "../util/BootstrapToast";
import axios from "axios";
export default {
  name: "register-user",
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
    BootstrapToast,
  },
  methods: {
    register() {
      axios
        .post("http://127.0.0.1:5000/api/register", {
          username: this.username,
          email: this.email,
          password: this.password,
          mobile: this.mobile,
          location: this.location,
          role: "user",
        })
        .then((res) => {
          if (res.status == 200) {
            this.$refs.toast.showCustomToast(res.data.msg, "success");
            setTimeout(() => {
              this.$router.push("/");
            }, 2000);
          } else {
            this.$refs.toast.showCustomToast(res.data.msg, "warning");
          }
        })
        .catch((err) => {
          console.log(err);
          this.$refs.toast.showCustomToast("Error in Registration", "danger");
        });
    },
  },
};
</script>
<style></style>
