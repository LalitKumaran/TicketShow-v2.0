<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Cancel Show</h3>
        <form @submit.prevent="cancelSlot">
          <div class="form-sub-container">
            <div>
              <div class="table-wrapper-scroll-x my-custom-scrollbar">
                <div
                  class="row justify-content-center p-3 m-2 text-warning bg-dark border border-warning rounded"
                >
                  <table class="table table-dark">
                    <tbody>
                      <tr>
                        <th class="text-warning">Movie</th>
                        <td class="text-warning">
                          {{ selectedMovie.show_name }}
                        </td>
                      </tr>
                      <tr>
                        <th class="text-warning">Theatre</th>
                        <td class="text-warning">
                          {{ selectedTheatre.venue_name }}
                        </td>
                      </tr>
                      <tr>
                        <th class="text-warning">Location</th>
                        <td class="text-warning">
                          {{ selectedTheatre.location }}
                        </td>
                      </tr>
                      <tr>
                        <th class="text-warning">Language</th>
                        <td class="text-warning">{{ selectedMovie.lang }}</td>
                      </tr>
                      <tr>
                        <th class="text-warning">Date</th>
                        <td class="text-warning">
                          {{ selectedSlot.date }}
                        </td>
                      </tr>
                      <tr>
                        <th class="text-warning">Time</th>
                        <td class="text-warning">
                          {{ selectedSlot.time }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="row justify-content-center">
                <button class="btn btn-outline-success m-1" type="submit">
                  Confirm
                </button>
                <button
                  @click="this.$router.push('/')"
                  class="btn btn-outline-danger m-1"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import axios from "axios";
import BootstrapToast from "../util/BootstrapToast";
export default {
  name: "cancel-slot",
  data() {
    return {
      slotId: "",
      movies: [],
      venues: [],
      slots: [],
      selectedMovie: {},
      selectedSlot: {},
      selectedTheatre: {},
    };
  },
  components: { Navbar, BootstrapToast },
  methods: {
    cancelSlot() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .delete(``, {
          headers,
        })
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
  },
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
<style></style>
