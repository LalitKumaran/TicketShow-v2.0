<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Delete Theatre</h3>
        <form @submit.prevent="deleteTheatre">
          <div class="form-sub-container">
            <div>
              <div class="table-wrapper-scroll-x my-custom-scrollbar">
                <div
                  class="row justify-content-center p-3 m-2 text-warning bg-dark border border-warning rounded"
                >
                  <table class="table table-dark">
                    <tbody>
                      <tr>
                        <th class="text-warning">Theatre</th>
                        <td class="text-warning">
                          {{ selectedTheatre.name }}
                        </td>
                      </tr>
                      <tr>
                        <th class="text-warning">Location</th>
                        <td class="text-warning">{{ selectedTheatre.city }}</td>
                      </tr>
                      <tr>
                        <th class="text-warning">Capacity</th>
                        <td class="text-warning">{{ selectedTheatre.seats }}</td>
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
  name: "delete-Theatre",
  data() {
    return {
      theatreId: "",
      theatres: [],
      selectedTheatre: {},
    };
  },
  components: {
    Navbar,
    BootstrapToast
  },
  methods: {
    deleteTheatre() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .delete(`http://127.0.0.1:5000/api/theatre/${this.theatreId}`, { headers })
        .then((res) => {
          console.log(res);
          this.$refs.toast.showCustomToast(res.data.msg, "success");
          setTimeout(() => {
            this.$router.push("/theatres");
          }, 3000);
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
          if (err.response) {
            this.$refs.toast.showCustomToast(
              err.response.data.error_message,
              "danger"
            );
          }
        });
    },
  },
  created() {
    this.theatreId = this.$route.params.theatreId;
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
        for (const theatre of this.theatres) {
          if (theatre.id == this.theatreId) {
            this.selectedTheatre = theatre;
            break;
          }
        }
        console.log(this.selectedTheatre)
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
