<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Update Movie</h3>
        <form @submit.prevent="updateMovie">
          <input
            v-model="movieName"
            type="text"
            placeholder="Movie name"
            id="moviename"
            required
          />

          <input
            v-model="rating"
            type="text"
            placeholder="Rating"
            id="rating"
          />

          <input
            v-model="genre"
            type="text"
            placeholder="Genre"
            id="genre"
          />

          <input
            v-model="cast"
            type="text"
            placeholder="Cast"
            id="cast"
          />

          <input
            v-model="language"
            type="text"
            placeholder="Language"
            id="language"
          />

          <input
            v-model="duration"
            type="text"
            placeholder="Duration"
            id="duration"
            disabled
          />

          <input id="image-label" placeholder="Poster" disabled />
          <input
            type="file"
            @change="getPoster"
            id="poster"
            accept="image/*"
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
  name: "update-movie",
  data() {
    return {
      venues: [],
      slots: [],
      movies: [],
      movieName: "",
      genre: "",
      rating: "",
      lang: "",
      cast: "",
      duration: "",
      poster: "",
      selectedMovie: {},
      movieId: "",
    };
  },
  components: { Navbar, BootstrapToast },
  methods: {
    getPoster(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.poster = reader.result;
      };
      reader.readAsDataURL(file);
    },
    updateMovie() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .put(
          "",
          {
            movieId: this.movieId,
            movieName: this.movieName,
            genre: this.genre,
            rating: this.rating,
            lang: this.lang,
            cast: this.cast,
            duration: this.duration,
            poster: this.poster,
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
  },
  created() {
    this.movieId = this.$route.params.movieId;
  },
};
</script>
<style></style>
