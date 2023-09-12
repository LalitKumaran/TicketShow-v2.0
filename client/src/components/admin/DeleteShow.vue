<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Delete Show</h3>
        <form @submit.prevent="deleteShow">
          <div class="select-wrapper">
            <select v-model="selectedShow" id="show" name="show">
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Show
              </option>
              <option style="color: #ffc107" v-if="shows.length == 0" disabled>
                No Show Available
              </option>
              <option
                style="color: #ffc107"
                v-for="show in shows"
                :value="show"
                :key="show.showId"
              >
                {{ show.showName }}
              </option>
            </select>
          </div>
          <button class="btn btn-outline-warning" type="submit">Delete</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import axios from "axios";
export default {
  name: "delete-show",
  data() {
    return {
      showId: "",
      shows: [],
      venues: [],
      slots: [],
      selectedShow: "",
    };
  },
  components: { Navbar },
  methods: {
    deleteShow() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .delete(``, {
          headers,
        })
        .then((res) => {
          console.log(res);
          setTimeout(() => {
            this.$router.push("/venues");
          }, 3000);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.showId = this.$route.params.showId;
  },
};
</script>
<style></style>
