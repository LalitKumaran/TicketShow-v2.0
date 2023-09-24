<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="container py-4">
      <div
        type="button"
        class="bg-dark p-2 w-100 rounded-top rounded-pill border-3 border-bottom border-warning"
      >
        <h5 class="form-inline text-warning">Welcome {{ user.username }}</h5>
      </div>
    </div>
    <div class="container bg-dark rounded p-1">
      <h5 class="card-title text-warning py-2">Upcoming</h5>
      <div v-if="upcomingBookings.length > 0">
        <div v-for:="myB in upcomingBookings">
          <div class="row m-4 p-2 border border-warning rounded">
            <div class="container">
              <h4 class="card-title text-warning pt-3">
                {{ myB.title }}
              </h4>
              <h6 class="card-title text-warning">
                {{ myB.name }}
              </h6>
              <h6 class="card-title text-warning pb-3">
                {{ myB.city }}
              </h6>
            </div>
            <div>
              <h5
                class="card-title text-warning border-top border-warning rounded p-3"
              ></h5>
            </div>
            <div class="container">
              <div class="container">
                <div class="row">
                  <h6 class="col-lg-4 text-warning">{{ myB.date }}</h6>
                  <h6 class="col-lg-4 text-warning">{{ myB.time }}</h6>
                  <h6 class="col-lg-4 text-warning">Rs.{{ myB.cost }}</h6>
                </div>
              </div>
              <div class="container">
                <h6 v-if="myB.status == 'Confirmed'" class="text-success">
                  {{ myB.status }}
                </h6>
                <h6 v-else-if="myB.status == 'Cancelled'" class="text-danger">
                  {{ myB.status }}
                </h6>
                <h6 class="text-secondary">
                  Booked on {{ myB.booked_date }}
                </h6>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div id="card" class="card m-2 bg-dark">
          <h5 class="text-secondary m-4 p-2">No Upcoming Booking</h5>
        </div>
      </div>
    </div>
    <div class="container bg-dark rounded p-1 my-2">
      <h5 class="card-title text-warning py-3">History</h5>
      <div v-if="historyBookings.length > 0">
        <div v-for:="myB in historyBookings">
          <div class="row m-4 p-2 border border-warning rounded">
            <div class="container">
              <h4 class="card-title text-warning pt-3">
                {{ myB.title }}
              </h4>
              <h6 class="card-title text-warning">
                {{ myB.name }}
              </h6>
              <h6 class="card-title text-warning pb-3">
                {{ myB.city }}
              </h6>
            </div>
            <div>
              <h5
                class="card-title text-warning border-top border-warning rounded p-3"
              ></h5>
            </div>
            <div class="container">
              <div class="container">
                <div class="row">
                  <h6 class="col-lg-4 text-warning">{{ myB.date }}</h6>
                  <h6 class="col-lg-4 text-warning">{{ myB.time }}</h6>
                  <h6 class="col-lg-4 text-warning">Rs.{{ myB.cost }}</h6>
                </div>
              </div>
              <div
                v-if="myB.status == 'Confirmed' && myB.user_rating == 0"
                class="text-warning"
              >
                <input
                  class="bg-dark text-warning border-0 border-bottom border-warning m-1"
                  v-model="myRating"
                  type="number"
                  min="1"
                  max="10"
                  style="font-style: italic"
                />&#9733;
                <button
                  @click="movieRating(myB)"
                  class="btn btn-outline-warning btn-sm"
                >
                  Rate
                </button>
              </div>
              <div v-else class="text-warning">
                Rated: {{ myB.user_rating }} &#9733;
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div id="card" class="card m-2 bg-dark">
          <h5 class="text-secondary m-4 p-2">No Booking History</h5>
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
  name: "profile-page",
  data() {
    return {
      user: {},
      bookings: [],
      slots: [],
      theatres: [],
      movies: [],
      myBookings: [],
      upcomingBookings: [],
      historyBookings: [],
      myRating: 0,
      minTime: currentTime,
      minDate: currentDate,
    };
  },
  components: {
    Navbar,
    BootstrapToast,
  },
  created() {
    this.user = JSON.parse(localStorage.getItem("user"));
  },
  methods: {
    movieRating(myB) {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .put(
          "http://127.0.0.1:5000/api/giveRating",
          {
            movie_id: myB.movie_id,
            booking_id: myB.booking_id,
            user_rating: this.myRating,
          },
          { headers }
        )
        .then((res) => {
          if (res.status == 200) {
            this.$refs.toast.showCustomToast(res.data.msg, "success");
            setTimeout(() => {
              this.$router.go(0);
            }, 2000);
          }
        })
        .catch((err) => {
          console.log(err);
        });
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
        console.log(res);
        this.bookings = JSON.parse(res.data.bookings);
        this.slots = JSON.parse(res.data.slots);
        this.theatres = JSON.parse(res.data.theatre);
        this.movies = JSON.parse(res.data.movie);
        const bookings = this.bookings.filter(
          (book) => book.user_id == this.user.user_id
        );
        for (const book of bookings) {
          const currentBooking = {};
          currentBooking.booking_id = book.booking_id;
          currentBooking.user_id = book.user_id;
          currentBooking.movie_id = book.movie_id;
          currentBooking.no_of_tickets = book.no_of_tickets;
          currentBooking.cost = book.cost;
          currentBooking.status = book.status;
          currentBooking.user_rating = book.user_rating;
          currentBooking.booked_date = book.booked_date;
          if (book.movie_id != null) {
            for (const movie of this.movies) {
              if (movie.id == book.movie_id) {
                currentBooking.title = movie.title;
                currentBooking.duration = movie.duration;
                break;
              }
            }
          } else {
            currentBooking.title = "NA";
            currentBooking.duration = "NA";
          }

          if (book.theatre_id != null) {
            for (const theatre of this.theatres) {
              if (theatre.id == book.theatre_id) {
                currentBooking.name = theatre.name;
                currentBooking.city = theatre.city;
                currentBooking.price = theatre.price;
                break;
              }
            }
          } else {
            currentBooking.name = "NA";
            currentBooking.city = "";
            currentBooking.price = "";
          }

          if (book.slot_id != null) {
            for (const slot of this.slots) {
              if (slot.id == book.slot_id) {
                currentBooking.date = slot.date;
                currentBooking.time = slot.time;
                break;
              }
            }
          } else {
            currentBooking.date = "";
            currentBooking.time = "";
          }

          this.myBookings.push(currentBooking);
          this.upcomingBookings = this.myBookings.filter(
            (myB) => myB.date > this.minDate || (myB.date == this.minDate && myB.time >= this.minTime)
          );
          this.historyBookings = this.myBookings.filter(
            (myB) => myB.date < this.minDate || (myB.date == this.minDate && myB.time < this.minTime)
          );
        }
      })
      .catch((err) => {
        console.log(err);
        this.$refs.toast.showCustomToast("Server Error", "warning");
        this.$router.push("/logout");
      });
  },
};
</script>
<style></style>
