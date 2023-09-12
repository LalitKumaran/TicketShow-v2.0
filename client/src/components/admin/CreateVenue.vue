<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Create Venue</h3>
        <form @submit.prevent="addVenue">
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

          <input id="image-label" placeholder="Image" disabled/>
          <input
            type="file"
            @change="getImage"
            accept="image/*"
            name="image"
            id="image"
          />
          <!-- <img :src="image" v-if="image" /> -->

          <button class="btn btn-outline-warning" type="submit">Create</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import axios from "axios";
export default {
  name: "create-venue",
  data() {
    return {
      user: "",
      name: "",
      location: "",
      capacity: "",
      price: "",
      image: "",
    };
  },
  components: {
    Navbar,
  },
  methods: {
    addVenue() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .post(
          "",
          {
            venueName: this.name,
            location: this.location,
            capacity: this.capacity,
            price: this.price,
            image: this.image,
          },
          { headers }
        )
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
    getImage(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.image = reader.result;
      };
      reader.readAsDataURL(file);
    },
  },
};
</script>
<style>
input::file-selector-button {
  color: #ffc107;
  background-color: #212529;
  border: 1px solid #ffc107;
  width: 100px;
  border-radius: 5px;
}
input::file-selector-button:hover {
  background-color: #ffc107;
  color: #212529;
}
input[type="file"] {
  padding: 10px;
}
#image-label{
  padding-bottom: 0;
  width: 300px;
  border: none
}
</style>
