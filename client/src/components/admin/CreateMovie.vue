<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Add Movie</h3>
        <form @submit.prevent="addMovie">
          <div class="select-wrapper">
            <select
              @change="getSelectedMovie"
              id="movie"
              v-model="selectedMovie"
              name="Movie"
            >
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Movie
              </option>
              <option style="color: #ffc107" :value="'new_movie'">
                New Movie
              </option>
              <option style="color: #ffc107" v-if="movies.length == 0" disabled>
                No Movie Available
              </option>
              <option
                style="color: #ffc107"
                v-for="movie in movies"
                :value="movie"
                :key="movie.show_id"
              >
                {{ movie.show_name }}
              </option>
            </select>
          </div>

          <div v-if="selectedMovie == 'new_movie'">
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
              v-model="genre"
              type="text"
              placeholder="Genre"
              name="genre"
              id="genre"
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
              placeholder="Language"
              name="language"
              id="language"
            />

            <input
              v-model="duration"
              type="text"
              placeholder="Duration"
              name="duration"
              id="duration"
              required
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
          </div>

          <div class="select-wrapper">
            <select id="theatre" name="theatre" required>
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
                :key="theatre.venue_id"
              >
                {{ theatre.venue_name }}
              </option>
            </select>
          </div>

          <input
            @change="slotAvailability"
            v-model="date"
            type="date"
            name="date"
            required
          />

          <!-- <input
            @change="slotAvailability"
            v-model="time"
            type="time"
            name="time"
            required
          /> -->

          <div class="select-wrapper">
            <select id="slot-time" name="slot-time" required>
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Slot
              </option>
              <option
                style="color: #ffc107"
                v-if="theatres.length == 0"
                disabled
              >
                No Slots Available
              </option>
              <option style="color: #ffc107">Morning-9:00 A.M</option>
              <option style="color: #ffc107">Noon-12:30 P.M</option>
              <option style="color: #ffc107">Matinee-4:00 P.M</option>
              <option style="color: #ffc107">Evening-7:30 P.M</option>
              <option style="color: #ffc107">Night-11:00 P.M</option>
            </select>
          </div>

          <p v-if="!isSlotAvailable" class="error-message">
            {{ slotErrorMessage }}
          </p>
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
export default {
  name: "create-Movie",
  data() {
    return {
      theatres: [],
      slots: [],
      movies: [],
      movieId: "",
      movieName: "",
      genre: "",
      rating: "",
      language: "",
      cast: "",
      duration: "",
      poster: "",
      selectedTheatre: {},
      selectedMovie: "",
      date: "",
      time: "",
      seats: "",
      isSlotAvailable: true,
      slotErrorMessage: "",
    };
  },
  components: {
    Navbar,
    BootstrapToast
  },
  methods: {
    getPoster(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.poster = reader.result;
      };
      reader.readAsDataURL(file);
    },
    addMovie() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .post(
          "",
          {
            movieId: this.movieId,
            movieName: this.movieName,
            genre: this.genre,
            rating: this.rating,
            language: this.language,
            cast: this.cast,
            duration: this.duration,
            poster: this.poster,
            theatre: this.selectedTheatre.theatreId,
            time: this.time,
            date: this.date,
            availableSeats: this.selectedTheatre.capacity,
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
    getSelectedMovie() {
      if (this.selectedMovie != "new_movie" && this.selectedMovie != "") {
        for (const movie of this.movies) {
          if (movie.movieId == this.selectedMovie.movieId) {
            this.movieId = movie.movieId;
            this.movieName = movie.movieName;
            this.genre = movie.genre;
            this.rating = movie.rating;
            this.lang = movie.lang;
            this.cast = movie.cast;
            this.duration = movie.duration;
            this.poster = movie.poster;
          }
        }
      } else {
        this.movieId = "";
        this.movieName = "";
        this.genre = "";
        this.rating = "";
        this.lang = "";
        this.cast = "";
        this.duration = "";
        this.poster = "";
      }
    },
    slotAvailability() {
      this.dayAvailability();
      const newSlotStartTime = new Date(`${this.date}T${this.time}`);
      for (const slot of this.slots) {
        if (this.selectedTheatre.theatreId == slot.theatreId) {
          const slotStartTime = new Date(`${slot.date}T${slot.time}`);
          const slotDuration = parseInt(slot.duration) * 60 * 1000;
          const slotEndTime = new Date(slotStartTime.getTime() + slotDuration);
          const newSlotEndTime = new Date(
            newSlotStartTime.getTime() +
              parseInt(this.duration.match(/\d+/)[0]) * 60 * 1000
          );
          this.isSlotAvailable = true;
          this.slotErrorMessage = "";
          if (
            (newSlotStartTime.getTime() < slotStartTime.getTime() &&
              newSlotEndTime.getTime() > slotStartTime.getTime()) ||
            (newSlotStartTime.getTime() > slotStartTime.getTime() &&
              newSlotStartTime.getTime() < slotEndTime.getTime())
          ) {
            this.time = null;
            this.isSlotAvailable = false;
            this.slotErrorMessage = `Slot ${this.date} ${slotStartTime}-${slotEndTime} at ${this.selectedTheatre.theatreName} Booked`;
            break;
          }
        }
      }
    },
    dayAvailability() {
      const newSlotStartTime = new Date(`${this.date}T${this.time}`);
      const averageDuration = 3 * 60 * 60 * 1000; // 3 hours in ms

      for (const slot of this.slots) {
        if (
          this.selectedTheatre.theatreId == slot.theatreId &&
          this.date == slot.date
        ) {
          const slotStartTime = new Date(`${slot.date}T${slot.time}`);
          const slotEndTime = new Date(
            slotStartTime.getTime() + averageDuration
          );
          const newSlotEndTime = new Date(
            newSlotStartTime.getTime() +
              parseInt(this.duration.match(/\d+/)[0]) * 60 * 1000
          );
          var availableTimePerDay = 24 * 60 * 60 * 1000;
          if (
            newSlotEndTime.getTime() > slotStartTime.getTime() ||
            (newSlotStartTime.getTime() > slotStartTime.getTime() &&
              newSlotStartTime.getTime() < slotEndTime.getTime())
          ) {
            availableTimePerDay -= parseInt(slot.duration) * 60 * 1000;
          }
        }
        const newSlotDuration =
          parseInt(this.duration.match(/\d+/)[0]) * 60 * 1000;
        if (availableTimePerDay < newSlotDuration) {
          this.date = null;
          this.isSlotAvailable = false;
          this.slotErrorMessage = `No Slot available at ${this.selectedTheatre.theatreName} on ${this.date}`;
        }
      }
    },
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
        this.theatres = res.data.venues;
        this.movies = res.data.shows;
        this.slots = res.data.slots;
        if (!res.data.success) {
          this.$refs.toast.showCustomToast(res.data.msg, "warning");
          setTimeout(() => {
            this.$router.push("/logout");
          }, 3000);
        }
      })
      .catch((err) => {
        console.log(err);
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
