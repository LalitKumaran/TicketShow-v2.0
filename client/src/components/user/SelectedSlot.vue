<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="view-slot bg-dark container my-2 p-3 rounded">
      <div>
        <div class="row">
          <h3 class="col-6 mx-4 border border-warning rounded p-2 text-warning">
            {{ selectedMovie.show_name }}
          </h3>
          <div
            class="col d-flex flex-row-reverse mx-2"
            v-if="user.role == 'admin'"
          >
            <router-link :to="'/delete-slot/' + slotId">
              <button class="btn btn-outline-danger mx-2">Cancel</button>
            </router-link>
          </div>
        </div>
        <div class="poster-container my-3">
          <img
            id="slot-poster"
            class="w-100"
            :src="'http://127.0.0.1:5000/images/' + selectedMovie.poster"
          />
        </div>
        <!-- <div class="table-wrapper-scroll-y my-custom-scrollbar"> -->
        <div
          class="row justify-content-center p-3 m-2 text-warning border border-warning rounded"
        >
          <table class="table table-dark">
            <tbody>
              <tr>
                <th class="text-warning">Rating</th>
                <td class="text-warning">{{ selectedMovie.rating }}</td>
              </tr>
              <tr>
                <th class="text-warning">Genre</th>
                <td class="text-warning">{{ selectedMovie.tag }}</td>
              </tr>
              <tr>
                <th class="text-warning">Cast</th>
                <td class="text-warning">{{ selectedMovie.cast }}</td>
              </tr>
              <tr>
                <th class="text-warning">Language</th>
                <td class="text-warning">{{ selectedMovie.lang }}</td>
              </tr>
              <tr>
                <th class="text-warning">Duration</th>
                <td class="text-warning">{{ selectedMovie.duration }}</td>
              </tr>
              <tr>
                <th class="text-warning">Date</th>
                <td class="text-warning">{{ selectedSlot.date }}</td>
              </tr>
              <tr>
                <th class="text-warning">Time</th>
                <td class="text-warning">{{ selectedSlot.time }}</td>
              </tr>
              <tr>
                <th class="text-warning">Venue</th>
                <td class="text-warning">{{ selectedTheatre.venue_name }}</td>
              </tr>
              <tr>
                <th class="text-warning">Location</th>
                <td class="text-warning">{{ selectedTheatre.location }}</td>
              </tr>
              <tr>
                <th class="text-warning">Seats Available</th>
                <td class="text-warning">{{ selectedSlot.seats_available }}</td>
              </tr>
              <tr>
                <th class="text-warning">Price</th>
                <td v-if="selectedMovie.rating < 6.0" class="text-warning">
                  {{ selectedTheatre.price }}
                  <i class="text-success">
                    Offer: {{ selectedTheatre.price - 20 }}</i
                  >
                </td>
                <td v-else-if="selectedMovie.rating > 9.0" class="text-warning">
                  {{ selectedTheatre.price + 20 }}
                </td>
                <td v-else class="text-warning">
                  {{ selectedTheatre.price }}
                </td>
              </tr>
              <tr>
                <th class="text-warning">Total Seats</th>
                <td v-if="selectedSlot.seats_available > 0">
                  <input
                    type="number"
                    step="1"
                    v-model="seatCount"
                    min="1"
                    :max="selectedSlot.seats_available"
                    id="seat-count"
                    class="text-center w-15 bg-dark border-warning rounded text-warning"
                  />
                </td>
                <td v-else>
                  <input
                    placeholder="Seats filled"
                    class="text-center bg-dark border-0 w-15"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- </div> -->
        <div class="row justify-content-center p-3">
          <div>
            <button
              v-if="
                selectedSlot.seats_available == 0 ||
                seatCount > selectedSlot.seats_available
              "
              class="w-100 btn bg-dark text-danger btn-outline-danger btn-lg"
            >
              Housefull
            </button>
            <router-link v-else :to="'/booking/' + slotId + '/' + seatCount">
              <button class="w-100 btn btn-outline-warning btn-lg">Book</button>
            </router-link>
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
export default {
  name: "selected-slot",
  data() {
    return {
      user: "",
      slotId: "",
      selectedSlot: {},
      selectedMovie: {},
      selectedTheatre: {},
      slots: [],
      theatres: [],
      movies: [],
      seatCount: 1,
    };
  },
  components: { Navbar, BootstrapToast },
  created() {
    this.slotId = this.$route.params.slotId;
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
        // if (!res.data.success) {
        //   this.$refs.toast.showCustomToast(res.data.msg, "warning");
        //   setTimeout(() => {
        //     this.$router.push("/logout");
        //   }, 3000);
        // } else {
        console.log(res.data);
        this.movies = res.data.shows;
        this.theatres = res.data.venues;
        this.slots = res.data.slots;
        for (const slot of this.slots) {
          if (this.slotId === slot.slot_id) {
            this.selectedSlot = slot;
            break;
          }
        }
        for (const movie of this.movies) {
          if (movie.show_id === this.selectedSlot.show_id) {
            this.selectedMovie = movie;
            break;
          }
        }
        for (const theatre of this.theatres) {
          if (theatre.venue_id === this.selectedSlot.venue_id) {
            this.selectedTheatre = theatre;
            break;
          }
          // }
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style>
.poster-container {
  display: flex;
  justify-content: center;
  border-radius: 10px;
}
#slot-poster {
  justify-content: center;
  margin: 0px 8px;
  object-fit: cover;
  border-radius: 10px;
}
</style>
