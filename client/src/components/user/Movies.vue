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
      <div class="row">
        <div
          v-for="movie in filteredMovies"
          @click="viewMovie"
          class="col-md-6 mb-4"
          :key="movie.show_id"
        >
          <div id="card" class="card m-2">
            <router-link :to="'/selected-movie/' + movie.show_id" class="elite-card">
              <div class="poster-container">
                <img
                  :src="'http://127.0.0.1:5000/images/' + movie.poster"
                  class="card-img elite-card-img"
                />
              </div>

              <div class="card-header elite-card-header">
                <h5 class="card-title text-warning">
                  {{ movie.show_name }}
                </h5>
                <div class="card-body text-warning">
                  <h6 class="card-subtitle mb-2">
                    {{ movie.rating }}<i style="color: #ffc107">&#9733;</i>
                  </h6>
                  <h6 class="card-subtitle mb-2">
                    {{ movie.tag }}
                  </h6>
                </div>
                <div class="card-body elite-buttons">
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/update-movie/' + movie.show_id"
                  >
                    <button class="btn btn-outline-warning mx-1 btn-dark-text">
                      Update
                    </button>
                  </router-link>
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/delete-movie/' + movie.show_id"
                  >
                    <button class="btn btn-outline-warning mx-1 btn-dark-text">
                      Delete
                    </button>
                  </router-link>
                </div>
              </div>
            </router-link>
          </div>
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
            m.show_name.toLowerCase().includes(newVal.toLowerCase()) ||
            m.tag.toLowerCase().includes(newVal.toLowerCase()) ||
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
        this.movies = res.data.shows;
        this.filteredMovies = res.data.shows;
        if (!res.data.success) {
          this.$refs.toast.showCustomToast(res.data.msg, "warning");
          setTimeout(() => {
            this.$router.push("/logout");
          }, 3000);
        }
        console.log(res.data.msg);
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style>
.poster-container {
  width: 100%;
  height: 150px;
  overflow: hidden;
}
</style>
