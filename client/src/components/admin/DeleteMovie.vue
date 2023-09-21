<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Delete Movie</h3>
        <form @submit.prevent="deleteMovie">
          <div class="form-sub-container">
            <div>
              <div class="table-wrapper-scroll-x my-custom-scrollbar">
                <div
                  class="row justify-content-center p-3 m-2 text-warning bg-dark border border-warning rounded"
                >
                  <table class="table table-dark">
                    <tbody>
                      <tr>
                        <th class="text-warning">Movie</th>
                        <td class="text-warning">
                          {{ selectedMovie.show_name }}
                        </td>
                      </tr>
                      <tr>
                        <th class="text-warning">Genre</th>
                        <td class="text-warning">{{ selectedMovie.rating }}</td>
                      </tr>
                      <tr>
                        <th class="text-warning">Language</th>
                        <td class="text-warning">{{ selectedMovie.lang }}</td>
                      </tr>
                      <tr>
                        <th class="text-warning">Duration</th>
                        <td class="text-warning">
                          {{ selectedMovie.duration }}
                        </td>
                      </tr>
                      <tr>
                        <th class="text-warning">Rating</th>
                        <td class="text-warning">
                          {{ selectedMovie.rating }} &#9733;
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="row justify-content-center">
                <button class="btn btn-outline-success m-1" type="submit">
                  Confirm
                </button>
                <button
                  @click="this.$router.push('/')"
                  class="btn btn-outline-danger m-1"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
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
  name: "delete-Movie",
  data() {
    return {
      movieId: "",
      movies: [],
      theatres: [],
      slots: [],
      selectedMovie: {},
    };
  },
  components: { Navbar, BootstrapToast },
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
  mounted() {
    this.user = JSON.parse(localStorage.getItem("user"));
    const accessToken = this.user.token;
    const headers = {
      Authorization: `Bearer ${accessToken}`,
    };
    axios
      .get("http://127.0.0.1:5000/api/fetch", { headers })
      .then((res) => {
        console.log(res.data.msg);
        console.log(res.data);
        this.theatres = res.data.venues;
        this.movies = res.data.shows;
        this.slots = res.data.slots;
        for (const movie of this.movies) {
          if (movie.show_id === this.movieId) {
            this.selectedMovie = movie;
            break;
          }
        }
      })
      .catch((err) => {
        console.log(err);
        // toast.error(err.response.data.msg);
        // if (err.response.status == 401) {
        //   setTimeout(() => {
        //     this.$router.push("/logout");
        //   }, 3000);
        // }
      });
  },
};
</script>
<style></style>
