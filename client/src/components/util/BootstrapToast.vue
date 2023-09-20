<template>
  <b-toast
    v-if="showToast"
    :auto-hide-delay="autoHideDelay"
    id="toast"
    :class="toastClass"
    @hidden="resetToast"
  >
    {{ message }}
    <button @click="resetToast" class="bg-dark btn btn-sm btn-outline-danger" id="close">X</button>
  </b-toast>
</template>

<script>
export default {
  name: "bootstrap-toast",
  data() {
    return {
      showToast: false,
      message: "",
      toastClass: '',
      autoHideDelay: 2000,
    };
  },
  methods: {
    showCustomToast(message, variant) {
      this.message = message;
      this.showToast = true;
      if (variant === "success") {
        this.toastClass = "bg-dark text-success border border-2 border-success";
      } else if (variant === "danger") {
        this.toastClass = "bg-dark text-danger border border-2 border-danger";
      } else if (variant === "info") {
        this.toastClass = "bg-dark text-info border border-2 border-info";
      } else if (variant === "warning") {
        this.toastClass = "bg-dark text-warning border border-2 border-warning";
      }
    },
    resetToast() {
      this.showToast = false;
      this.message = "";
      this.toastClass="";
    },
  },
};
</script>
<style scoped>
#toast {
  position: fixed;
  top: 60px;
  right: 0px;
  transform: translateX(-50%);
  background-color: #212729;
  padding: 10px 20px;
  border-radius: 10px;
}

@media (max-width: 768px) {
  #toast {
    top: auto;
    bottom: 10px;
    left: 10px;
    right: 10px;
    transform: none;
  }
}
#close{
  border: none
}
</style>
