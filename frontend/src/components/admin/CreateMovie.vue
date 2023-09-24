<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Add Movie</h3>
        <form @submit.prevent="addMovie">
          <div> 
            <input
              v-model="title"
              type="text"
              placeholder="Title"
              id="title"
              required
            />

            <input
              v-model="rating"
              type="text"
              placeholder="Rating"
              id="rating"
            />

            <input v-model="genre" type="text" placeholder="Genre" id="genre" />

            <input
              v-model="director"
              type="text"
              placeholder="Director"
              id="director"
            />

            <input v-model="stars" type="text" placeholder="Stars" id="stars" />

            <input
              v-model="language"
              type="text"
              placeholder="Language"
              id="language"
            />

            <input
              v-model="duration"
              type="text"
              placeholder="Duration(mins)"
              id="duration"
              required
            />

            <input id="image-label" placeholder="Poster" disabled />
            <input
              type="file"
              @change="getPoster"
              id="image"
              accept="image/*"
            />
          </div>
          <button class="btn btn-outline-warning" type="submit">Add</button>
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
  name: "create-Movie",
  data() {
    return {
      theatres: [],
      slots: [],
      movies: [],
      movieId: "",
      title: "",
      genre: "",
      rating: "",
      language: "",
      director: "",
      stars: "",
      duration: "",
      image: "",
      selectedMovie: "",
    }
  },
  components: {
    Navbar,
    BootstrapToast,
  },
  methods: {
    getPoster(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.image = reader.result;
      };
      reader.readAsDataURL(file);
    },
    addMovie() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .post(
          "http://127.0.0.1:5000/api/movie",
          {
            title: this.title,
            genre: this.genre,
            rating: this.rating,
            language: this.language,
            director: this.director,
            stars: this.stars,
            duration: this.duration,
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
          if (err.response) {
            this.$refs.toast.showCustomToast(
              err.response.data.error_message,
              "danger"
            );
          }
        });
    },
  },
  beforeMount() {
    this.user = JSON.parse(localStorage.getItem("user"));
    const accessToken = this.user.token;
    const headers = {
      Authorization: `Bearer ${accessToken}`,
    };
    axios
      .get("http://127.0.0.1:5000/api/fetch", { headers })
      .then((res) => {
        console.log(res.data);
        this.theatres = JSON.parse(res.data.theatre);
        this.movies = JSON.parse(res.data.movie);
        this.slots = JSON.parse(res.data.slots);
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style>
.form-subcontainer select {
  display: block;
  border: none;
  outline: none;
  border-bottom: 2px solid #ffc107;
  background-color: #212529;
  padding: 10px;
  margin: 10px 0;
  color: #ffc107;
  width: 300px;
}
.form-subcontainer input::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
.form-subcontainer input::-webkit-clock {
  filter: invert(1);
}
</style>
