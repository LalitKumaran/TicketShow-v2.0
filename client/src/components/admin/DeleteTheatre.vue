<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Delete Theatre</h3>
        <form @submit.prevent="deleteTheatre">
          <div class="select-wrapper">
            <select v-model="selectedTheatre" id="theatre" name="theatre">
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Theatre
              </option>
              <option style="color: #ffc107" v-if="theatres.length == 0" disabled>
                No Theatre Available
              </option>
              <option
                style="color: black"
                v-for="theatre in theatres"
                :value="theatre"
                :key="theatre.theatreId"
              >
                {{ theatre.theatreName }}
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
  name: "delete-Theatre",
  data() {
    return {
      theatreId: "",
      shows: [],
      theatres: [],
      slots: [],
      selectedTheatre: "",
    };
  },
  components: {
    Navbar,
  },
  methods: {
    deleteTheatre() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .delete("", { headers })
        .then((res) => {
          setTimeout(() => {
            this.$router.push("/theatres");
          }, 3000);
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.theatreId = this.$route.params.theatreId;
  },
};
</script>
<style></style>
