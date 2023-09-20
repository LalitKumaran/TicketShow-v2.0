<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Delete Movie</h3>
        <form @submit.prevent="deleteMovie">
          <div class="select-wrapper">
            <select v-model="selectedMovie" id="Movie" name="Movie">
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Movie
              </option>
              <option style="color: #ffc107" v-if="movies.length == 0" disabled>
                No Movie Available
              </option>
              <option
                style="color: #ffc107"
                v-for="movie in movies"
                :value="movie"
                :key="movie.movieId"
              >
                {{ movie.movieName }}
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
  name: "delete-Movie",
  data() {
    return {
      movieId: "",
      movies: [],
      venues: [],
      slots: [],
      selectedMovie: "",
    };
  },
  components: { Navbar },
  methods: {
    deleteMovie() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .delete(``, {
          headers,
        })
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
