<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Update Venue</h3>
        <form @submit.prevent="updateVenue">
          <input
            type="text"
            v-model="name"
            placeholder="Venue Name"
            name="venuename"
            id="venuename"
          />

          <input
            type="text"
            v-model="capacity"
            placeholder="Capacity"
            name="capacity"
            id="capacity"
          />
          <input
            type="text"
            v-model="location"
            placeholder="Location"
            name="location"
            id="location"
          />

          <input
            type="number"
            v-model="price"
            placeholder="Ticket Price"
            min="0"
            name="price"
            id="price"
          />

          <input id="image-label" placeholder="Image" disabled />
          <input
            type="file"
            placeholder="Image"
            @change="getImage"
            accept="image/*"
            name="image"
            id="image"
          />

          <!-- <img :src="image" v-if="image" /> -->

          <button class="btn btn-outline-warning" type="submit">Update</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import axios from "axios";
export default {
  name: "update-venue",
  data() {
    return {
      user: {},
      name: "",
      location: "",
      capacity: "",
      price: "",
      image: "",
      venueId: "",
      selectedVenue: {},
    };
  },
  components: {
    Navbar,
  },
  methods: {
    updateVenue() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .put(
          "",
          {
            venueId: this.vid,
            venueName: this.name,
            location: this.location,
            capacity: this.capacity,
            price: this.price,
            image: this.image,
          },
          { headers }
        )
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
    getImage(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.image = reader.result;
      };
      reader.readAsDataURL(file);
    },
  },
  created() {
    this.venueId = this.$route.params.venueId;
  },
};
</script>
<style></style>
