<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Create Theatre</h3>
        <form @submit.prevent="addTheatre">
          <input
            type="text"
            v-model="name"
            placeholder="Theatre Name"
            id="theatrename"
          />

          <input
            type="text"
            v-model="seats"
            placeholder="Capacity"
            id="seats"
          />
          <input type="text" v-model="city" placeholder="Location" id="city" />

          <input
            type="number"
            v-model="price"
            placeholder="Ticket Price"
            min="0"
            id="price"
          />

          <input id="image-label" placeholder="Image" disabled />
          <input type="file" @change="getImage" accept="image/*" id="image" />
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
import BootstrapToast from "../util/BootstrapToast.vue";
export default {
  name: "create-Theatre",
  data() {
    return {
      user: "",
      name: "",
      city: "",
      seats: "",
      price: "",
      image: "",
    };
  },
  components: {
    Navbar,
    BootstrapToast,
  },
  methods: {
    addTheatre() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .post(
          "http://127.0.0.1:5000/api/theatre",
          {
            name: this.name,
            city: this.city,
            seats: this.seats,
            price: this.price,
            image: this.image,
          },
          { headers }
        )
        .then((res) => {
          this.$refs.toast.showCustomToast(res.data.msg, "success");
          setTimeout(() => {
            this.$router.push("/theatres");
          }, 3000);
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
          if (err.response) {
            this.$refs.toast.showCustomToast(
              err.response.data.error_message,
              "danger"
            );
          }
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
  width: 120px;
  border-radius: 5px;
}
input::file-selector-button:hover {
  background-color: #ffc107;
  color: #212529;
}
input[type="file"] {
  padding: 10px;
}
#image-label {
  padding-bottom: 0;
  width: 300px;
  border: none;
}
</style>
