<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-container bg-dark rounded">
        <h2 class="text-center text-warning m-3">Payment</h2>
        <div class="form-sub-container">
          <div>
            <div class="table-wrapper-scroll-x my-custom-scrollbar">
              <div
                class="row justify-content-center p-3 m-2 text-warning bg-dark border border-warning rounded"
              >
                <table class="table table-dark">
                  <thead>
                    <tr>
                      <th>Movie Title</th>
                      <td>
                        {{ selectedMovie.title }}
                      </td>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th>Date</th>
                      <td>{{ selectedSlot.date }}</td>
                    </tr>
                    <tr>
                      <th>Time</th>
                      <td>{{ selectedSlot.time }}</td>
                    </tr>
                    <tr>
                      <th>Theatre</th>
                      <td>{{ selectedTheatre.name }}</td>
                    </tr>
                    <tr>
                      <th>Location</th>
                      <td>{{ selectedTheatre.city }}</td>
                    </tr>
                    <tr>
                      <th>Seats</th>
                      <td>{{ seatCount }}</td>
                    </tr>
                    <tr>
                      <th>Amount</th>
                      <td>{{ cost }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="row justify-content-center px-3 py-3">
              <button
                @click="confirmBooking"
                class="btn btn-outline-success my-3 btn-lg"
              >
                Pay
              </button>
              <button
                @click="this.$router.push('/')"
                class="btn btn-outline-danger btn-lg"
              >
                Cancel
              </button>
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
export default {
  name: "booking-page",
  data() {
    return {
      movies: [],
      theatres: [],
      slots: [],
      slotId: "",
      seatCount: 0,
      cost: 0,
      selectedMovie: {},
      selectedSlot: {},
      selectedTheatre: {},
    };
  },
  components: { Navbar, BootstrapToast },
  methods: {
    confirmBooking() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .post(
          "http://127.0.0.1:5000/api/booking",
          {
            email: this.user.email,
            date: this.selectedSlot.date,
            time: this.selectedSlot.time,
            no_of_tickets: this.seatCount,
            cost: this.cost,
            slot_id: this.slotId,
          },
          { headers }
        )
        .then((res) => {
          if (res.data.success == "true") {
            this.$refs.toast.showCustomToast(res.data.msg, "success");
          } else {
            this.$refs.toast.showCustomToast(res.data.msg, "warning");
          }
          setTimeout(() => {
            this.$router.push("/profile");
          }, 3000);
        })
        .catch((err) => {
          console.log(err);

        });
    },
  },
  created() {
    this.slotId = this.$route.params.slotId;
    this.seatCount = this.$route.params.seatCount;
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
            if (this.selectedMovie.rating < 6) {
              this.cost = (theatre.price - 20) * this.seatCount;
            } else if (this.selectedMovie.rating > 6) {
              this.cost = (theatre.price + 20) * this.seatCount;
            } else {
              this.cost = theatre.price * this.seatCount;
            }
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
<style></style>
