<template>
  <div>
    <router-view />
  </div>
</template>

<script>
// import Navbar from "../src/components/util/Navbar.vue";
export default {
  name: "App",
};
</script>

<style>
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  font-family: 'Courier New', Courier, monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
input,select{
  outline: none
}
</style>
