<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Delete Venue</h3>
        <form @submit.prevent="deleteVenue">
          <div class="select-wrapper">
            <select v-model="selectedVenue" id="venue" name="venue">
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Venue
              </option>
              <option style="color: #ffc107" v-if="venues.length == 0" disabled>
                No Venue Available
              </option>
              <option
                style="color: black"
                v-for="venue in venues"
                :value="venue"
                :key="venue.venueId"
              >
                {{ venue.venueName }}
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
  name: "delete-venue",
  data() {
    return {
      venueId: "",
      shows: [],
      venues: [],
      slots: [],
      selectedVenue: "",
    };
  },
  components: {
    Navbar,
  },
  methods: {
    deleteVenue() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .delete("", { headers })
        .then((res) => {
          setTimeout(() => {
            this.$router.push("/venues");
          }, 3000);
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.venueId = this.$route.params.venueId;
  },
};
</script>
<style></style>
