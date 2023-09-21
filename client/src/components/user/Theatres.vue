<template>
  <div>
    <Navbar />
    <bootstrap-toast ref="toast"></bootstrap-toast>
    <div class="search">
      <input
        class="form-control bg-dark text-light m-1 w-75 border border-warning"
        type="search"
        id="search"
        v-model="searchFilter"
        placeholder="&#128269;  Search by theatres, location"
        aria-label="Search"
      />
    </div>
    <div class="container py-4">
      <div type="button" class="bg-dark text-warning p-2 w-100 rounded-pill">
        <h5 class="form-inline">Theatres</h5>
      </div>
      <div class="row">
        <div
          v-for="theatre in filteredTheatres"
          @click="viewTheatre"
          class="col-md-6 mb-4"
          :key="theatre.venue_id"
        >
          <div id="card" class="card m-2">
            <router-link
              :to="'/selected-theatre/' + theatre.venue_id"
              class="elite-card"
            >
              <div class="image-container">
                <img
                  :src="'http://127.0.0.1:5000/images/' + theatre.image"
                  class="card-img elite-card-img"
                />
              </div>

              <div class="card-header elite-card-header">
                <h5 class="card-title text-warning">
                  {{ theatre.venue_name }}
                </h5>
                <div class="card-body text-warning">
                  <h6 class="card-subtitle mb-2">
                    {{ theatre.location }}
                  </h6>
                </div>
                <div class="card-body elite-buttons">
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/update-theatre/' + theatre.venue_id"
                  >
                    <button class="btn btn-outline-warning btn-dark-text">
                      Update
                    </button>
                  </router-link>
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/delete-theatre/' + theatre.venue_id"
                  >
                    <button class="btn btn-outline-warning mx-1 btn-dark-text">
                      Delete
                    </button>
                  </router-link>
                  <router-link v-if="user.role == 'admin'" :to="''">
                    <button
                      @click="exportStats(theatre)"
                      class="btn btn-outline-warning btn-dark-text"
                    >
                      &#8689; Export
                    </button>
                  </router-link>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import BootstrapToast from "../util/BootstrapToast";
import axios from "axios";
export default {
  name: "theatres-page",
  data() {
    return {
      user: "",
      theatres: [],
      searchFilter: "",
      filteredTheatres: [],
    };
  },
  components: {
    Navbar,
    BootstrapToast,
  },
  watch: {
    searchFilter(newVal) {
      if (newVal === "") {
        this.filteredTheatres = this.theatres;
      } else {
        this.filteredTheatres = this.theatres.filter(
          (t) =>
            t.venue_name.toLowerCase().includes(newVal.toLowerCase()) ||
            t.location.toLowerCase().includes(newVal.toLowerCase())
        );
      }
    },
  },
  methods: {
    exportStats(theatre) {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .post(
          `http://127.0.0.1:5000/exportvenue`,
          { user: this.user, venue: theatre },
          { headers }
        )
        .then((res) => {
          if (res.status == 200) {
            localStorage.setItem("task_id", res.data.task_id);
            this.checkStatus(res.data.task_id);
            console.log(res.data.task_id);
          }
        })
        .catch((err) => {
          console.log(err);
          // if (err.response.status == 401) {
          //   this.$refs.toast.showCustomToast(res.data.msg, "warning");
          //   setTimeout(() => {
          //     this.$router.push("/logout");
          //   }, 3000);
          // }
        });
    },
    checkStatus(task_id) {
      const interval = setInterval(() => {
        this.user = JSON.parse(localStorage.getItem("user"));
        const accessToken = this.user.token;
        const headers = {
          Authorization: `Bearer ${accessToken}`,
        };
        axios
          .get(`http://127.0.0.1:5000/exportvenue/checkstatus/${task_id}`, {
            headers,
          })
          .then((res) => {
            if (res.status == 200) {
              if (res.data.ready == "true") {
                clearInterval(interval);
                localStorage.removeItem("task_id");
                if (res.data.success == "true") {
                  this.$refs.toast.showCustomToast(res.data.msg, "success");
                } else {
                  this.$refs.toast.showCustomToast(res.data.msg, "danger");
                }
              }
            }
          })
          .catch((err) => {
            console.log(err);
            // if (err.response.status == 401) {
            //   this.$refs.toast.showCustomToast(res.data.msg, "danger");
            //   setTimeout(() => {
            //     this.$router.push("/logout");
            //   }, 3000);
            // }
          });
      }, 3000);
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
        this.theatres = res.data.venues;
        this.filteredTheatres = res.data.venues;
        if (!res.data.success) {
          this.$refs.toast.showCustomToast(res.data.msg, "warning");
          setTimeout(() => {
            this.$router.push("/logout");
          }, 3000);
        }
        console.log(res.data.msg);
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style>
#search::placeholder {
  color: gray;
}

#card {
  margin: 10px 0;
}

.image-container {
  width: 100%;
  height: 220px;
  overflow: hidden;
}

.card-header {
  border-top: 1px solid #ffc107;
  border-radius: 10px 10px 0 0;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.form-control::-webkit-input-placeholder {
  color: grey;
}

.btn-white-text:hover {
  color: white !important;
}

.elite-card {
  background-color: #212729;
  border: 1px solid #ffc107;
  border-radius: 10px;
  padding: 10px;
  transition: background-color 0.3s ease;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.elite-card:hover {
  box-shadow: 0px 0px 10px #ffc107;
}

.elite-card-img {
  border-radius: 10px 10px 0 0;
}

.elite-card-header {
  padding: 10px;
  width: 100%;
}

.elite-card-title {
  font-size: 1.5rem;
}

.elite-card-subtitle {
  font-size: 1.2rem;
}

.elite-buttons {
  margin-top: 1rem;
  text-align: center;
}

.btn-white-text {
  color: white;
}
</style>
