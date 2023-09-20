<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Login</h3>
        <form @submit.prevent="login">
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
            v-model="password"
            autocomplete="on"
            required
          />
          <button class="btn btn-outline-warning" type="submit">Login</button>
          <p class="text-warning">
            New user?
            <router-link class="text-warning" to="/register"
              >Register</router-link
            >
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
  name: "log-in",
  data() {
    return {
      user: {},
      email: "",
      password: "",
    };
  },
  components: {
    Navbar,
    BootstrapToast,
  },
  methods: {
    login() {
      axios
        .post("http://127.0.0.1:5000/api/login", {
          email: this.email,
          password: this.password,
        })
        .then((res) => {
          this.user = JSON.parse(res.data.user);
          if (res.status == 200) {
          this.$refs.toast.showCustomToast(res.data.msg, "success");
          localStorage.setItem("user", res.data.user);
            setTimeout(() => {
              this.$router.push("/theatres");
            }, 2000);
          } else {
            this.$refs.toast.showCustomToast(res.data.msg, "warning");
          }
        })
        .catch((err) => {
          console.log(err);
          this.$refs.toast.showCustomToast('Error in Authentication', "warning");
        });
    },
  },
};
</script>
<style>
.form-container {
  display: grid;
  justify-content: center;
  margin-top: 30px;
  padding: 20px;
}
.form-subcontainer {
  background-color: #212529;
  padding: 40px;
  border-radius: 10px;
}
.form-subcontainer input {
  display: block;
  border: none;
  outline: none;
  border-bottom: 2px solid #ffc107;
  background-color: #212529;
  padding: 10px;
  margin: 10px 0;
  color: #ffc107;
  width: 300px;
}
.form-subcontainer button {
  margin: 20px 0;
  width: 100px;
}
body {
  background-image: url("../../assets/bg1.jpg");
}
</style>
