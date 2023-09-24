<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
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
import BootstrapToast from "../util/BootstrapToast";
export default {
  name: "create-admin",
  data() {
    return {
      username: "",
      email: "",
      password: "",
    };
  },
  components: {
    Navbar,
    BootstrapToast
  },
  methods: {
    register() {
      axios
        .post("http://127.0.0.1:5000/api/register", {
          username: this.username,
          email: this.email,
          password: this.password,
          role: "admin",
        })
        .then((res) => {
          setTimeout(() => {
            this.$router.push("/theatres");
          }, 2000);
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
          this.$refs.toast.showCustomToast("Server Error", "warning");
          this.$router.push("/logout");
        });
    },
  },
};
</script>
<style></style>
