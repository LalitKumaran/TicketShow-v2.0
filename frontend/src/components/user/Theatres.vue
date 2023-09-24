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
        placeholder="&#128269;  Search by theatres, city"
        aria-label="Search"
      />
    </div>
    <div class="container py-4">
      <div type="button" class="bg-dark text-warning p-2 w-100 rounded-pill">
        <h5 class="form-inline">Theatres</h5>
      </div>
      <div v-if="filteredTheatres.length > 0" class="row">
        <div
          v-for="theatre in filteredTheatres"
          @click="viewTheatre"
          class="col-md-6 mb-4"
          :key="theatre.id"
        >
          <div id="card" class="card m-2">
            <router-link
              :to="'/selected-theatre/' + theatre.id"
              class="elite-card"
            >
              <div class="image-container">
                <img
                  :src="'http://127.0.0.1:5000/images/theatre/' + theatre.image"
                  class="card-img elite-card-img"
                />
              </div>

              <div class="card-header elite-card-header">
                <h5 class="card-title text-warning">
                  {{ theatre.name }}
                </h5>
                <div class="card-body text-warning">
                  <h6 class="card-subtitle mb-2">
                    {{ theatre.city }}
                  </h6>
                </div>
                <div class="card-body elite-buttons">
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/update-theatre/' + theatre.id"
                  >
                    <button class="btn btn-outline-warning btn-dark-text">
                      Update
                    </button>
                  </router-link>
                  <router-link
                    v-if="user.role == 'admin'"
                    :to="'/delete-theatre/' + theatre.id"
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
      <div v-else>
        <div id="card" class="card m-2 bg-dark">
          <h5 class="text-secondary m-4 p-2">No Theatres Available</h5>
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
            t.name.toLowerCase().includes(newVal.toLowerCase()) ||
            t.city.toLowerCase().includes(newVal.toLowerCase())
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
          `http://127.0.0.1:5000/exportStats`,
          { user: this.user, theatre: theatre },
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
          .get(`http://127.0.0.1:5000/exportStats/checkStatus/${task_id}`, {
            headers,
          })
          .then((res) => {
            if (res.status == 200) {
              if (res.data.ready == "true") {
                localStorage.removeItem("task_id");
                if (res.data.success == "true") {
                  this.$refs.toast.showCustomToast(res.data.msg, "success");
                } else {
                  this.$refs.toast.showCustomToast(res.data.msg, "danger");
                }
              }
            }
            clearInterval(interval);
          })
          .catch((err) => {
            console.log(err);
            clearInterval(interval);
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
        this.theatres = JSON.parse(res.data.theatre);
        this.filteredTheatres = JSON.parse(res.data.theatre);
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
        this.$refs.toast.showCustomToast("Server Error", "warning");
        this.$router.push("/logout");
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
