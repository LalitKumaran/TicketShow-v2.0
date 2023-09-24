<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Add Show</h3>
        <form @submit.prevent="addSlot">
          <div class="select-wrapper">
            <select id="movie" value="selectedMovie">
              <option style="color: #ffc107" value="selectedMovie" selected>
                {{ selectedMovie.title }}
              </option>
            </select>
          </div>

          <div class="select-wrapper">
            <select id="theatre" v-model="selectedTheatre" required>
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Theatre
              </option>
              <option
                style="color: #ffc107"
                v-if="theatres.length == 0"
                disabled
              >
                No theatre Available
              </option>
              <option
                style="color: #ffc107"
                v-for="theatre in theatres"
                :value="theatre"
                :key="theatre.id"
              >
                {{ theatre.name }}
              </option>
            </select>
          </div>

          <input v-model="date" :min="minDate" type="date" required />

          <div class="select-wrapper">
            <select id="slot-time" v-model="time" required>
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Slot
              </option>
              <option
                style="color: #ffc107"
                v-if="filteredTimeSlots.length == 0"
                disabled
              >
                No Slots Available
              </option>
              <option
                style="color: #ffc107"
                v-else
                v-for="fTS in filteredTimeSlots"
                :value="fTS[1]"
                :key="fTS[1]"
              >
                {{ fTS[0] }} - {{ fTS[1] }}
              </option>
            </select>
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
  name: "create-Movie",
  data() {
    return {
      theatres: [],
      slots: [],
      movies: [],
      movieId: "",
      selectedTheatre: "",
      selectedMovie: "",
      date: "",
      time: "",
      seats: "",
      timeSlots: [
        ["Morning", "09:00"],
        ["Noon", "12:30"],
        ["Matinee", "16:00"],
        ["Evening", "19:30"],
        ["Night", "23:00"],
      ],
      filteredTimeSlots: [],
      minTime: currentTime,
      minDate: currentDate,
    };
  },
  components: {
    Navbar,
    BootstrapToast,
  },
  watch: {
    date(newVal) {
      this.filteredTimeSlots = this.timeSlots;
      if (newVal !== "") {
        for (const slot of this.slots) {
          if (slot.id == this.selectedTheatre.id && slot.date == newVal) {
            this.filteredTimeSlots = this.filteredTimeSlots.filter(
              (t) => t[1] !== slot.date
            );
          }
        }
      }
      console.log("slots", this.filteredTimeSlots);
    },
  },
  methods: {
    addSlot() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      console.log(this.selectedTheatre);
      axios
        .post(
          "http://127.0.0.1:5000/api/slot",
          {
            movie_id: this.movieId,
            theatre_id: this.selectedTheatre.id,
            time: this.time,
            date: this.date,
            remaining_seats: this.selectedTheatre.seats,
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
          else{
            this.$refs.toast.showCustomToast("Server Error", "warning");
            this.$router.push("/logout");
          }
        });
    },
  },
  created() {
    this.movieId = this.$route.params.movieId;
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
        for (const movie of this.movies) {
          if (movie.id == this.movieId) {
            this.selectedMovie = movie;
            break;
          }
        }
        console.log(this.selectedMovie);
      })
      .catch((err) => {
        console.log(err);
        this.$refs.toast.showCustomToast("Server Error", "warning");
        this.$router.push("/logout");
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
