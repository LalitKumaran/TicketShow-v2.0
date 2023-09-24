<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Update Movie</h3>
        <form @submit.prevent="updateMovie">
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
          />

          <input id="image-label" placeholder="Poster" disabled />
          <input type="file" @change="getPoster" id="image" accept="image/*" />
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
      title: "",
      genre: "",
      rating: "",
      language: "",
      director: "",
      stars: "",
      duration: "",
      image: "",
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
        this.image = reader.result;
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
          `http://127.0.0.1:5000/api/movie/${this.movieId}`,
          {
            title: this.title,
            genre: this.genre,
            director: this.director,
            stars: this.stars,
            language: this.language,
            duration: this.duration,
            rating: this.rating,
            image: this.image,
            showing: 1,
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
        });
    },
  },
  created() {
    this.movieId = this.$route.params.movieId;
  },
  mounted() {
    this.user = JSON.parse(localStorage.getItem("user"));
    const accessToken = this.user.token;
    const headers = {
      Authorization: `Bearer ${accessToken}`,
    };
    axios
      .get("http://127.0.0.1:5000/api/fetch", { headers })
      .then((res) => {
        this.theatres = JSON.parse(res.data.theatre);
        this.movies = JSON.parse(res.data.movie);
        this.slots = JSON.parse(res.data.slots);
        for (const movie of this.movies) {
          if (movie.id == this.movieId) {
            this.selectedMovie = movie;
            break;
          }
        }

        this.movie_id = this.selectedMovie.id;
        this.title = this.selectedMovie.title;
        this.genre = this.selectedMovie.genre;
        this.rating = this.selectedMovie.rating;
        this.language = this.selectedMovie.language;
        this.director = this.selectedMovie.director;
        this.stars = this.selectedMovie.stars;
        this.duration = this.selectedMovie.duration;
        this.image = this.selectedMovie.image;
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
};
</script>
<style></style>
