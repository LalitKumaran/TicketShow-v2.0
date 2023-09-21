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
      <div v-for:="myB in myBookings">
        <div class="row m-4 p-2 border border-warning rounded">
          <div class="container">
            <h4 class="card-title text-warning pt-3">
              {{ myB.show_name }}
            </h4>
            <h6 class="card-title text-warning">
              {{ myB.venue_name }}
            </h6>
            <h6 class="card-title text-warning pb-3">
              {{ myB.location }}
            </h6>
          </div>
          <!-- <div class="poster-container my-3">
            <img
              id="slot-poster"
              class="w-100"
              :src="'http://127.0.0.1:5000/images/' + myB.poster"
            />
          </div> -->
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
                <h6 class="col-lg-4 text-warning">Rs.{{ myB.amount }}</h6>
              </div>
            </div>
            <div class="container">
              <h6 v-if="myB.status == 'Confirmed'" class="text-success">
                {{ myB.status }}
              </h6>
              <h6 v-else-if="myB.status == 'Cancelled'" class="text-danger">
                {{ myB.status }}
              </h6>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container bg-dark rounded p-1 my-2">
      <h5 class="card-title text-warning py-3">History</h5>
      <div v-for:="myB in myBookings">
        <div class="row m-4 p-2 border border-warning rounded">
          <div class="container">
            <h4 class="card-title text-warning pt-3">
              {{ myB.show_name }}
            </h4>
            <h6 class="card-title text-warning">
              {{ myB.venue_name }}
            </h6>
            <h6 class="card-title text-warning pb-3">
              {{ myB.location }}
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
                <h6 class="col-lg-4 text-warning">Rs.{{ myB.amount }}</h6>
              </div>
            </div>
            <div v-if="myB.status=='Confirmed' && myB.user_rating == 0" class="text-warning">
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
            <div v-else class="text-warning">Rated: {{ myB.user_rating }} &#9733;</div>
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
          "http://127.0.0.1:5000/api/ratebooking",
          {
            show_id: myB.show_id,
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
          // this.$refs.toast.showCustomToast(res.data.msg, "warning");
          // if (err.response.status == 401) {
          //   setTimeout(() => {
          //     this.$router.push("/logout");
          //   }, 3000);
          // }
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
        console.log(res.data.msg);
        this.bookings = res.data.bookings;
        this.slots = res.data.slots;
        this.theatres = res.data.venues;
        this.movies = res.data.shows;
        const bookings = this.bookings.filter(
          (book) => book.user_id == this.user.email
        );
        for (const book of bookings) {
          const currentBooking = {};
          currentBooking.booking_id = book.booking_id;
          currentBooking.user_id = book.user_id;
          currentBooking.show_id = book.show_id;
          currentBooking.seat_count = book.seat_count;
          currentBooking.amount = book.amount;
          currentBooking.status = book.status;
          currentBooking.user_rating = book.user_rating;
          currentBooking.msg = book.msg;
          currentBooking.date = book.date;
          currentBooking.time = book.time;
          if (book.show_id != null) {
            for (const movie of this.movies) {
              if (movie.show_id == book.show_id) {
                currentBooking.show_name = movie.show_name;
                currentBooking.duration = movie.duration;
                break;
              }
            }
          } else {
            currentBooking.show_name = "NA";
            currentBooking.duration = "NA";
          }

          if (book.venue_id != null) {
            for (const theatre of this.theatres) {
              if (theatre.venue_id == book.venue_id) {
                currentBooking.venue_name = theatre.venue_name;
                currentBooking.location = theatre.location;
                currentBooking.price = theatre.price;
                break;
              }
            }
          } else {
            currentBooking.venue_name = "NA";
            currentBooking.location = "";
            currentBooking.price = "";
          }
          this.myBookings.push(currentBooking);
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
