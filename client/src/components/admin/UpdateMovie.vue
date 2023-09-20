<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Update Movie</h3>
        <form @submit.prevent="updateMovie">
          <input
            v-model="movieName"
            type="text"
            placeholder="Movie name"
            name="moviename"
            id="moviename"
            required
          />

          <input
            v-model="rating"
            type="text"
            placeholder="Rating"
            name="rating"
            id="rating"
          />

          <input
            v-model="tag"
            type="text"
            placeholder="Tags"
            name="tag"
            id="tag"
          />

          <input
            v-model="cast"
            type="text"
            placeholder="Cast"
            name="cast"
            id="cast"
          />

          <input
            v-model="language"
            type="text"
            placeholder="language"
            name="language"
            id="language"
          />

          <input
            v-model="duration"
            type="text"
            placeholder="Duration"
            name="duration"
            id="duration"
            disabled
          />

          <input id="image-label" placeholder="Poster" disabled />
          <input
            type="file"
            @change="getPoster"
            name="poster"
            id="poster"
            accept="image/*"
          />
          <!-- <img v-if="poster" :src="poster" /> -->

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
  name: "update-movie",
  data() {
    return {
      venues: [],
      slots: [],
      movies: [],
      movieName: "",
      tag: "",
      rating: "",
      lang: "",
      cast: "",
      duration: "",
      poster: "",
      selectedMovie: {},
      movieId: "",
    };
  },
  components: { Navbar },
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
            tag: this.tag,
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
