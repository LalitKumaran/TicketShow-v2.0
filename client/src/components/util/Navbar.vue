<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <!-- <img class="logo my-1 mx-2" :src="require('../../assets/logo.png')" /> -->
    <button
      class="navbar-toggler mx-4"
      type="button"
      data-toggle="collapse"
      data-target="#navbar"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div
      class="collapse navbar-collapse flex justify-content-end mx-4 px-0"
      id="navbar"
    >
      <div class="navbar-nav justify-content-end">
        <router-link
          v-if="isUserAlive"
          class="nav-text nav-item nav-link"
          id="Venue"
          to="/venues"
          >Venues</router-link
        >
        <router-link
          v-if="isUserAlive"
          class="nav-item nav-link"
          id="shows"
          to="/shows"
          >Shows</router-link
        >
        <router-link
          v-if="isAdminAlive"
          class="nav-item nav-link"
          id="create-show"
          to="/add-show"
          >Create Show</router-link
        >
        <router-link
          v-if="isAdminAlive"
          class="nav-item nav-link"
          id="create-venue"
          to="/add-venue"
          >Create Venue</router-link
        >
        <router-link
          v-if="isAdminAlive"
          class="nav-item nav-link"
          id="create-admin"
          to="/create-admin"
          >Create Admin</router-link
        >
        <router-link
          v-if="isUserAlive"
          class="nav-item nav-link"
          id="profile"
          to="/profile"
          >Profile</router-link
        >
        <router-link
          v-if="isUserAlive"
          class="nav-item nav-link"
          id="logout"
          to="/logout"
          >Logout</router-link
        >
        <router-link
          v-if="!isUserAlive"
          class="nav-item nav-link"
          id="login"
          to="/"
          >Login</router-link
        >
        <router-link
          v-if="!isUserAlive"
          class="nav-item nav-link"
          id="register"
          to="/register"
          >Register</router-link
        >
      </div>
    </div>
  </nav>
</template>
<script>
export default {
  name: "nav-bar",
  computed: {
    isUserAlive() {
      return localStorage.getItem("user") !== null;
    },
    isAdminAlive() {
      const user = JSON.parse(localStorage.getItem("user"));
      return user && user.role === "admin";
    },
  },
};
</script>
<style scoped>
.nav-item {
  color: #ffc107;
  font-size: 18px;
}
</style>
