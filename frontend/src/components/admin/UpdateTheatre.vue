<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Update Theatre</h3>
        <form @submit.prevent="updateTheatre">
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
          <input
            type="file"
            placeholder="Image"
            @change="getImage"
            accept="image/*"
            id="image"
          />
          <button class="btn btn-outline-warning" type="submit">Update</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import axios from "axios";
import BootstrapToast from "../util/BootstrapToast";
export default {
  name: "update-theatre",
  data() {
    return {
      user: {},
      name: "",
      city: "",
      seats: "",
      price: "",
      image: "",
      theatreId: "",
      selectedTheatre: {},
    };
  },
  components: {
    Navbar,
    BootstrapToast,
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
          `http://127.0.0.1:5000/api/theatre/${this.theatreId}`,
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
          console.log(res);
          this.$refs.toast.showCustomToast(res.data.msg, "success");
          setTimeout(() => {
            this.$router.push("/theatres");
          }, 3000);
        })
        .catch((err) => {
          console.log(err);
          if (err.response) {
            this.$refs.toast.showCustomToast(
              err.response.data.error_message,
              "danger"
            );
          }
          else{
            this.$refs.toast.showCustomToast("Server Error", "warning");
            this.$router.push("/logout");
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
  created() {
    this.theatreId = this.$route.params.theatreId;
  },
  mounted() {
    document.body.classList.add("update-venue-background");
    this.user = JSON.parse(localStorage.getItem("user"));
    const accessToken = this.user.token;
    const headers = {
      Authorization: `Bearer ${accessToken}`,
    };
    axios
      .get("http://127.0.0.1:5000/api/fetch", { headers })
      .then((res) => {
        console.log(res)
        this.theatres = JSON.parse(res.data.theatre);
        this.movies = JSON.parse(res.data.movie);
        this.slots = JSON.parse(res.data.slots);
        for (const theatre of this.theatres) {
          if (theatre.id == this.theatreId) {
            this.selectedTheatre = theatre;
            break;
          }
        }
        console.log(this.selectedTheatre)
        this.name = this.selectedTheatre.name;
        this.city = this.selectedTheatre.city;
        this.seats = this.selectedTheatre.seats;
        this.price = this.selectedTheatre.price;
        this.image = this.selectedTheatre.image;
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style></style>
