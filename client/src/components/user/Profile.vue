<template>
  <div><Navbar />
    <div class="container py-4">
      <div type="button" class="bg-dark text-warning p-2 w-100 rounded-top rounded-pill">
        <h5 class="form-inline">Welcome {{ user.username }}</h5>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
export default {
  name: "profile-page",
  data() {
    return {
      user: {},
    };
  },
  components: {
    Navbar,
  },
};
</script>
<style></style>
