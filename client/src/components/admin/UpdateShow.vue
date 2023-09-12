<template>
  <div>
    <Navbar />
    <div class="form-container">
      <div class="form-subcontainer">
        <h3 class="text-warning">Update Show</h3>
        <form @submit.prevent="UpdateShow">
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
            disabled
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

          <button class="btn btn-outline-warning" type="submit">Update</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../util/Navbar";
import axios from "axios";
export default {
  name: "update-show",
  data() {
    return {
      venues: [],
      slots: [],
      shows: [],
      showName: "",
      tag: "",
      rating: "",
      lang: "",
      cast: "",
      duration: "",
      poster: "",
      selectedShow: {},
      showId: "",
    };
  },
  components: { Navbar },
  methods: {
    getPoster(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.poster = reader.result;
      };
      reader.readAsDataURL(file);
    },
    updateShow() {
      this.user = JSON.parse(localStorage.getItem("user"));
      const accessToken = this.user.token;
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .put(
          "",
          {
            showId: this.showId,
            showName: this.showName,
            tag: this.tag,
            rating: this.rating,
            lang: this.lang,
            cast: this.cast,
            duration: this.duration,
            poster: this.poster,
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
  },
  created() {
    this.showId = this.$route.params.showId;
  },
};
</script>
<style></style>
