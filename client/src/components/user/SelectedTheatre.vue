<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="row m-1 p-1 search">
      <input
        class="col-lg-7 bg-dark text-warning m-1 p-1 border-1 border-warning rounded"
        type="search"
        id="search"
        v-model="searchFilter"
        placeholder="&#128269;  Search by movies, genre, ratings"
        aria-label="Search"
      />
      <div class="col">
        <div class="row">
          <select
            v-model="time"
            class="text-warning m-1 p-1 col bg-dark border-1 border-warning rounded"
          >
            <option :value="''" default>All shows</option>
            <option :value="'morning'">Morning</option>
            <option :value="'noon'">Noon</option>
            <option :value="'matinee'">Matinee</option>
            <option :value="'evening'">Evening</option>
            <option :value="'night'">Night</option>
          </select>
          <input
            v-model="date"
            type="date"
            :min="minDate"
            placeholder="Today"
            class="text-warning m-1 p-1 col bg-dark border-1 border-warning rounded"
          />
        </div>
      </div>
    </div>
    <div class="container py-4">
      <div
        type="button"
        class="bg-dark text-warning p-2 w-100 rounded-top border-bottom border-4 border-warning rounded-pill"
      >
        <h5 class="form-inline">{{ selectedTheatre.venue_name }}</h5>
      </div>
    </div>
    <div class="container bg-dark rounded p-1">
      <div v-for:="movie in searchFilteredMovies">
        <div class="row m-4 p-2 border border-warning rounded">
          <div class="poster-container my-3">
            <img
              id="slot-poster"
              class="w-100"
              :src="'http://127.0.0.1:5000/images/' + movie.poster"
            />
          </div>
          <div>
            <h5 class="card-title text-warning border-top border-warning rounded pt-3">
              {{ movie.show_name }}
            </h5>
            <h6 class="card-title text-warning pb-3">
              {{ movie.rating }} &#9733;
            </h6>
          </div>
          <div class="container">
            <div class="d-flex m-2">
              <div v-for:="slot in filteredSlots" :key="slot.slot_id">
                <router-link :to="'/selected-slot/' + slot.slot_id">
                  <div v-if:="slot.show_id == movie.show_id">
                    <button class="btn btn-outline-success p-2 m-2">
                      {{ slot.time }}
                    </button>
                    <!-- <button class="btn btn-outline-danger p-2 m-2">
                    {{ slot.time }}
                  </button> -->
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Navbar from "../util/Navbar";
import BootstrapToast from "../util/BootstrapToast";

const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, "0"); // Months are zero-based, so we add 1
const day = String(today.getDate()).padStart(2, "0");

// const hours = today.getHours().toString().padStart(2, "0");
// const minutes = today.getMinutes().toString().padStart(2, "0");
// const seconds = today.getSeconds().toString().padStart(2, '0');

// const currentTime = `${hours}:${minutes}`;
const currentDate = `${year}-${month}-${day}`;

export default {
  name: "selected-theatre",
  data() {
    return {
      user: {},
      theatreId: "",
      movies: [],
      theatres: [],
      slots: [],
      selectedTheatre: {},
      date: currentDate,
      time: "",
      // st_time: "00:00",
      // end_time: "23:59",
      minDate: currentDate,
      // minTime: currentTime,
      filteredMovies: [],
      searchFilteredMovies: [],
      filteredSlots: [],
      searchFilter: "",
    };
  },
  components: { Navbar, BootstrapToast },
  watch: {
    searchFilter(newVal) {
      if (newVal === "") {
        this.searchFilteredMovies = this.movies;
      } else {
        this.searchFilteredMovies = this.movies.filter(
          (m) =>
            m.show_name.toLowerCase().includes(newVal.toLowerCase()) ||
            m.tag.toLowerCase().includes(newVal.toLowerCase()) ||
            m.rating == newVal
        );
      }
    },
  },
  created() {
    this.theatreId = this.$route.params.theatreId;
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
        this.theatres = res.data.venues;
        this.movies = res.data.shows;
        this.slots = res.data.slots;
        for (const theatre of this.theatres) {
          if (theatre.venue_id === this.theatreId) {
            this.selectedTheatre = theatre;
            break;
          }
        }
        for (const slot of this.slots) {
          if (slot.venue_id == this.theatreId) {
            if (!this.filteredSlots.includes(slot)) {
              this.filteredSlots.push(slot);
            }
            for (const movie of this.movies) {
              if (
                slot.show_id == movie.show_id &&
                !this.filteredMovies.includes(movie)
              ) {
                this.filteredMovies.push(movie);
              }
            }
          }
        }
        this.filteredSlots.sort((s1, s2) => {
          if (s1.date === s2.date) {
            return s1.time.localeCompare(s2.time);
          } else {
            return s1.date.localeCompare(s2.date);
          }
        });
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
    this.searchFilteredMovies = this.filteredMovies;
  },
};
</script>
<style>
input::-webkit-calendar-picker-indicator {
  filter: invert(1);
  color: #ffc107;
}
</style>
