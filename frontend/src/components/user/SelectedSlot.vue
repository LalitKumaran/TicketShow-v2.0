<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="view-slot bg-dark container my-2 p-3 rounded">
      <div>
        <div class="row">
          <h3 class="col-6 mx-4 border border-warning rounded p-2 text-warning">
            {{ selectedMovie.title }}
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
        <div class="image-container1 my-3">
          <img
            id="slot-image"
            class="w-75"
            :src="'http://127.0.0.1:5000/images/movie/' + selectedMovie.image"
          />
        </div>
        <div class="table-wrapper-scroll-y my-custom-scrollbar">
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
                  <td class="text-warning">{{ selectedMovie.genre }}</td>
                </tr>
                <tr>
                  <th class="text-warning">Director</th>
                  <td class="text-warning">{{ selectedMovie.director }}</td>
                </tr>
                <tr>
                  <th class="text-warning">Stars</th>
                  <td class="text-warning">{{ selectedMovie.stars }}</td>
                </tr>
                <tr>
                  <th class="text-warning">Language</th>
                  <td class="text-warning">{{ selectedMovie.language }}</td>
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
                  <td class="text-warning">{{ selectedTheatre.name }}</td>
                </tr>
                <tr>
                  <th class="text-warning">Location</th>
                  <td class="text-warning">{{ selectedTheatre.city }}</td>
                </tr>
                <tr>
                  <th class="text-warning">Seats Available</th>
                  <td class="text-warning">
                    {{ selectedSlot.remaining_seats }}
                  </td>
                </tr>
                <tr>
                  <th class="text-warning">Price</th>
                  <td v-if="selectedMovie.rating < 6.0" class="text-warning">
                    {{ selectedTheatre.price }}
                    <i class="text-success">
                      Offer: {{ selectedTheatre.price - 20 }}</i
                    >
                  </td>
                  <td
                    v-else-if="selectedMovie.rating > 9.0"
                    class="text-warning"
                  >
                    {{ selectedTheatre.price + 20 }}
                  </td>
                  <td v-else class="text-warning">
                    {{ selectedTheatre.price }}
                  </td>
                </tr>
                <tr>
                  <th class="text-warning">Total Seats</th>
                  <td v-if="selectedSlot.remaining_seats > 0">
                    <input
                      type="number"
                      step="1"
                      v-model="seatCount"
                      min="1"
                      :max="selectedSlot.remaining_seats"
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
        </div>
        <div class="row justify-content-center p-3">
          <div>
            <button
              v-if="
                selectedSlot.remaining_seats == 0 ||
                seatCount > selectedSlot.remaining_seats
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
        console.log(res);
        this.movies = JSON.parse(res.data.movie);
        this.theatres = JSON.parse(res.data.theatre);
        this.slots = JSON.parse(res.data.slots);
        for (const slot of this.slots) {
          if (this.slotId == slot.id) {
            this.selectedSlot = slot;
            break;
          }
        }
        for (const movie of this.movies) {
          if (movie.id == this.selectedSlot.movie_id) {
            this.selectedMovie = movie;
            break;
          }
        }
        for (const theatre of this.theatres) {
          if (theatre.id == this.selectedSlot.theatre_id) {
            this.selectedTheatre = theatre;
            break;
          }
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style>
.image-container1 {
  display: flex;
  justify-content: center;
  border-radius: 10px;
  height: 250px;
}
#slot-image {
  justify-content: center;
  margin: 0px 8px;
  object-fit: cover;
  border-radius: 10px;
}
</style>
