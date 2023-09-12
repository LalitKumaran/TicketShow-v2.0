<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Add Show</h3>
        <form @submit.prevent="addShow">
          <div class="select-wrapper">
            <select
              @change="getSelectedShow"
              id="show"
              v-model="selectedShow"
              name="show"
            >
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Show
              </option>
              <option style="color: #ffc107" :value="'new_show'">
                New Show
              </option>
              <option style="color: #ffc107" v-if="shows.length == 0" disabled>
                No Show Available
              </option>
              <option
                style="color: #ffc107"
                v-for="show in shows"
                :value="show"
                :key="show.showId"
              >
                {{ show.showName }}
              </option>
            </select>
          </div>

          <div v-if="selectedShow == 'new_show'">
            <input
              v-model="showName"
              type="text"
              placeholder="Show name"
              name="showname"
              id="showname"
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
            <select id="venue" name="venue" required>
              <option style="color: #ffc107" value="" selected disabled hidden>
                Select Venue
              </option>
              <option style="color: #ffc107" v-if="venues.length == 0" disabled>
                No Venue Available
              </option>
              <option
                style="color: #ffc107"
                v-for="venue in venues"
                :value="venue"
                :key="venue.venueId"
              >
                {{ venue.venueName }}
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

          <input
            @change="slotAvailability"
            v-model="time"
            type="time"
            name="time"
            required
          />

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
export default {
  name: "create-show",
  data() {
    return {
      venues: [],
      slots: [],
      shows: [],
      showId: "",
      showName: "",
      tag: "",
      rating: "",
      language: "",
      cast: "",
      duration: "",
      poster: "",
      selectedVenue: {},
      selectedShow: "",
      date: "",
      time: "",
      seats: "",
      isSlotAvailable: true,
      slotErrorMessage: "",
    };
  },
  components: {
    Navbar,
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
    addShow() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .post(
          "",
          {
            showId: this.showId,
            showName: this.showName,
            tag: this.tag,
            rating: this.rating,
            language: this.language,
            cast: this.cast,
            duration: this.duration,
            poster: this.poster,
            venue: this.selectedVenue.venueId,
            time: this.time,
            date: this.date,
            availableSeats: this.selectedVenue.capacity,
          },
          { headers }
        )
        .then((res) => {
          console.log(res);
          setTimeout(() => {
            this.$router.push("/venues");
          }, 3000);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getSelectedShow() {
      if (this.selectedShow != "new_show" && this.selectedShow != "") {
        for (const show of this.shows) {
          if (show.showId == this.selectedShow.showId) {
            this.showId = show.showId;
            this.showName = show.showName;
            this.tag = show.tag;
            this.rating = show.rating;
            this.lang = show.lang;
            this.cast = show.cast;
            this.duration = show.duration;
            this.poster = show.poster;
          }
        }
      } else {
        this.showId = "";
        this.showName = "";
        this.tag = "";
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
        if (this.selectedVenue.venueId == slot.venueId) {
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
            this.slotErrorMessage = `Slot ${this.date} ${slotStartTime}-${slotEndTime} at ${this.selectedVenue.venueName} Booked`;
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
          this.selectedVenue.venueId == slot.venueId &&
          this.date == slot.date
        ) {
          const slotStartTime = new Date(`${slot.date}T${slot.time}`);
          const slotEndTime = new Date(slotStartTime.getTime() + averageDuration);
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
          this.slotErrorMessage = `No Slot available at ${this.selectedVenue.venueName} on ${this.date}`;
        }
      }
    },
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
