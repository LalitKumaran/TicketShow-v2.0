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
        placeholder="&#128269;  Search by theatres, city"
        aria-label="Search"
      />
      <div class="col">
        <div class="row">
          <select
            v-model="timeFilter"
            class="text-warning m-1 p-1 col bg-dark border-1 border-warning rounded"
          >
            <option :value="''" default>All shows</option>
            <option :value="'09:00'">Morning</option>
            <option :value="'12:30'">Noon</option>
            <option :value="'16:00'">Matinee</option>
            <option :value="'19:30'">Evening</option>
            <option :value="'23:00'">Night</option>
          </select>
          <input
            v-model="dateFilter"
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
        <h5 class="form-inline">{{ selectedMovie.title }}</h5>
      </div>
    </div>

    <div class="container bg-dark rounded p-1">
      <div v-if="searchFilteredTheatres.length > 0">
        <div v-for:="theatre in searchFilteredTheatres">
          <div class="row m-4 p-2 border border-warning rounded">
            <div class="row">
              <h5 class="card-title text-warning pt-3">
                {{ theatre.name }}
              </h5>
              <h6 class="card-title text-warning pb-3">
                {{ theatre.city }}
              </h6>
            </div>
            <div class="container border-top border-warning rounded">
              <div class="d-flex m-2">
                <div v-for:="slot in filteredSlots" :key="slot.id">
                  <router-link :to="'/selected-slot/' + slot.id">
                    <div
                      v-if:="
                        slot.theatre_id == theatre.id &&
                        slot.date == dateFilter &&
                        (timeFilter == '' || slot.time == timeFilter) &&
                        (slot.date > minDate ||
                          (slot.date == minDate && slot.time >= minTime))
                      "
                    >
                      <button
                        v-if="slot.remaining_seats > 0"
                        class="btn btn-outline-success p-2 m-2"
                      >
                        {{ slot.time }}
                      </button>
                      <button v-else class="btn btn-outline-danger p-2 m-2">
                        {{ slot.time }}
                      </button>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>
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
import axios from "axios";
import Navbar from "../util/Navbar";
import BootstrapToast from "../util/BootstrapToast";

const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, "0"); // Months are zero-based, so we add 1
const day = String(today.getDate()).padStart(2, "0");

const hours = today.getHours().toString().padStart(2, "0");
const minutes = today.getMinutes().toString().padStart(2, "0");
// const seconds = today.getSeconds().toString().padStart(2, '0');

const currentTime = `${hours}:${minutes}`;
const currentDate = `${year}-${month}-${day}`;

export default {
  name: "selected-movie",
  data() {
    return {
      user: {},
      movieId: "",
      movies: [],
      theatres: [],
      slots: [],
      selectedMovie: {},
      minDate: currentDate,
      minTime: currentTime,
      filteredTheatres: [],
      searchFilteredTheatres: [],
      filteredSlots: [],
      searchFilter: "",
      timeFilter: "",
      dateFilter: currentDate,
    };
  },
  components: { Navbar, BootstrapToast },
  watch: {
    searchFilter(newVal) {
      if (newVal === "") {
        this.filteredTheatres = this.theatres;
      } else {
        this.filteredTheatres = this.theatres.filter(
          (t) =>
            t.name.toLowerCase().includes(newVal.toLowerCase()) ||
            t.city.toLowerCase().includes(newVal.toLowerCase())
        );
      }
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
        console.log(res);
        this.theatres = JSON.parse(res.data.theatre);
        this.movies = JSON.parse(res.data.movie);
        this.slots = JSON.parse(res.data.slots);
        for (const movie of this.movies) {
          if (movie.id == this.movieId) {
            this.selectedMovie = movie;
            break;
          }
        }
        for (const slot of this.slots) {
          if (slot.movie_id == this.movieId) {
            if (!this.filteredSlots.includes(slot)) {
              this.filteredSlots.push(slot);
            }
            for (const theatre of this.theatres) {
              if (
                slot.theatre_id == theatre.id &&
                !this.filteredTheatres.includes(theatre)
              ) {
                this.filteredTheatres.push(theatre);
              }
            }
            this.searchFilteredTheatres = this.filteredTheatres;
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
        this.$refs.toast.showCustomToast("Server Error", "warning");
        this.$router.push("/logout");
      });
    this.searchFilteredTheatres = this.filteredTheatres;
  },
};
</script>
<style></style>
