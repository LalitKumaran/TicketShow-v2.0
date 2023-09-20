<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Update Theatre</h3>
        <form @submit.prevent="updateTheatre">
          <input
            type="text"
            v-model="name"
            placeholder="Theatre Name"
            name="theatrename"
            id="theatrename"
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
  name: "update-theatre",
  data() {
    return {
      user: {},
      name: "",
      location: "",
      capacity: "",
      price: "",
      image: "",
      TheatreId: "",
      selectedTheatre: {},
    };
  },
  components: {
    Navbar,
  },
  methods: {
    updateTheatre() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .put(
          "",
          {
            theatreId: this.vid,
            theatreName: this.name,
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
            this.$router.push("/theatres");
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
    this.theatreId = this.$route.params.theatreId;
  },
};
</script>
<style></style>
