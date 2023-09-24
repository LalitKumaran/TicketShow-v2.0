<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="search">
      <input
        class="form-control bg-dark text-light m-1 w-75 border border-warning"
        type="search"
        id="search"
        v-model="searchFilter"
        placeholder="&#128269;  Search by movies, genre, ratings"
        aria-label="Search"
      />
    </div>
    <div class="container py-4">
      <div type="button" class="bg-dark text-warning p-2 w-100 rounded-pill">
        <h5 class="form-inline">Movies</h5>
      </div>
      <div v-if="filteredMovies.length > 0" class="row">
        <div
          v-for="movie in filteredMovies"
          @click="viewMovie"
          class="col-md-6 mb-4"
          :key="movie.id"
        >
          <div id="card" class="card m-2">
            <router-link :to="'/selected-movie/' + movie.id" class="elite-card">
              <div class="image-container1">
                <img
                  :src="'http://127.0.0.1:5000/images/movie/' + movie.image"
                  class="card-img elite-card-img"
                />
              </div>

              <div class="card-header elite-card-header">
                <h5 class="card-title text-warning">
                  {{ movie.title }}
                </h5>
                <div class="card-body text-warning">
                  <h6 class="card-subtitle mb-2">
                    {{ movie.rating }}<i style="color: #ffc107">&#9733;</i>
                  </h6>
                  <h6 class="card-subtitle mb-2">
                    {{ movie.genre }}
                  </h6>
                </div>
                <div class="card-body elite-buttons">
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/update-movie/' + movie.id"
                  >
                    <button class="btn btn-outline-warning mx-1 btn-dark-text">
                      Update
                    </button>
                  </router-link>
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/delete-movie/' + movie.id"
                  >
                    <button class="btn btn-outline-warning mx-1 btn-dark-text">
                      Delete
                    </button>
                  </router-link>
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/add-show/' + movie.id"
                  >
                    <button class="btn btn-outline-warning mx-1 btn-dark-text">
                      AddShow
                    </button>
                  </router-link>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
      <div v-else>
        <div id="card" class="card m-2 bg-dark">
          <h5 class="text-secondary m-4 p-2">No Movies Available</h5>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import BootstrapToast from "../util/BootstrapToast";
import axios from "axios";
export default {
  name: "shows-page",
  data() {
    return {
      user: "",
      movies: [],
      searchFilter: "",
      filteredMovies: [],
    };
  },
  components: {
    Navbar,
    BootstrapToast,
  },
  watch: {
    searchFilter(newVal) {
      if (newVal === "") {
        this.filteredMovies = this.movies;
      } else {
        this.filteredMovies = this.movies.filter(
          (m) =>
            m.title.toLowerCase().includes(newVal.toLowerCase()) ||
            m.genre.toLowerCase().includes(newVal.toLowerCase()) ||
            m.rating == newVal
        );
      }
    },
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
        this.movies = JSON.parse(res.data.movie);
        this.filteredMovies = JSON.parse(res.data.movie);
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style>
.image-container1 {
  width: 100%;
  height: 150px;
  overflow: hidden;
}
</style>
