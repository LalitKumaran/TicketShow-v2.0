import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import CreateAdmin from "./components/admin/CreateAdmin";
import CreateMovie from "./components/admin/CreateMovie";
import CreateTheatre from "./components/admin/CreateTheatre";
import UpdateMovie from "./components/admin/UpdateMovie";
import UpdateTheatre from "./components/admin/UpdateTheatre";
import DeleteMovie from "./components/admin/DeleteMovie";
import DeleteTheatre from "./components/admin/DeleteTheatre";
import DeleteSlot from "./components/admin/DeleteSlot";
import Movies from "./components/user/Movies";
import Theatres from "./components/user/Theatres";
import SelectedMovie from "./components/user/SelectedMovie";
import SelectedTheatre from "./components/user/SelectedTheatre";
import SelectedSlot from "./components/user/SelectedSlot";
import Booking from "./components/user/Booking";
import Profile from "./components/user/Profile";

const isUserAlive = () => {
  return localStorage.getItem("user") !== null;
};

const isAdminAlive = () => {
  const user = JSON.parse(localStorage.getItem("user"));
  return user && user.role === "admin";
};

const routes = [
  {
    path: "/",
    name: "log-in",
    component: Login,
    beforeEnter: (to, from, next) => {
      if (isUserAlive()) {
        next("/theatres");
      } else {
        next();
      }
    },
  },
  {
    path: "/register",
    name: "sign-up",
    component: Register,
  },
  {
    path: "/create-admin",
    name: "create-admin",
    component: CreateAdmin,
    beforeEnter: (to, from, next) => {
      if (isAdminAlive()) {
        next();
      } else if (isUserAlive()) {
        console.log("Admin access only");
      } else {
        next("/");
      }
    },
  },
  {
    path: "/add-movie",
    name: "create-movie",
    component: CreateMovie,
    beforeEnter: (to, from, next) => {
      if (isAdminAlive()) {
        next();
      } else if (isUserAlive()) {
        console.log("Admin access only");
      } else {
        next("/");
      }
    },
  },
  {
    path: "/add-theatre",
    name: "create-theatre",
    component: CreateTheatre,
    beforeEnter: (to, from, next) => {
      if (isAdminAlive()) {
        next();
      } else if (isUserAlive()) {
        console.log("Admin access only");
      } else {
        next("/");
      }
    },
  },
  {
    path: "/update-movie/:movieId",
    name: "update-movie",
    component: UpdateMovie,
    beforeEnter: (to, from, next) => {
      if (isAdminAlive()) {
        next();
      } else if (isUserAlive()) {
        console.log("Admin access only");
      } else {
        next("/");
      }
    },
  },
  {
    path: "/update-theatre/:theatreId",
    name: "update-theatre",
    component: UpdateTheatre,
    beforeEnter: (to, from, next) => {
      if (isAdminAlive()) {
        next();
      } else if (isUserAlive()) {
        console.log("Admin access only");
      } else {
        next("/");
      }
    },
  },
  {
    path: "/delete-movie/:movieId",
    name: "Delete-Movie",
    component: DeleteMovie,
    beforeEnter: (to, from, next) => {
      if (isAdminAlive()) {
        next();
      } else if (isUserAlive()) {
        console.log("Admin access only");
      } else {
        next("/");
      }
    },
  },
  {
    path: "/delete-theatre/:theatreId",
    name: "delete-theatre",
    component: DeleteTheatre,
    beforeEnter: (to, from, next) => {
      if (isAdminAlive()) {
        next();
      } else if (isUserAlive()) {
        console.log("Admin access only");
      } else {
        next("/");
      }
    },
  },
  {
    path: "/delete-slot/:slotId",
    name: "delete-slot",
    component: DeleteSlot,
    beforeEnter: (to, from, next) => {
      if (isAdminAlive()) {
        next();
      } else if (isUserAlive()) {
        console.log("Admin access only");
      } else {
        next("/");
      }
    },
  },
  {
    path: "/movies",
    name: "movies-page",
    component: Movies,
    beforeEnter: (to, from, next) => {
      if (isUserAlive()) {
        next();
      } else {
        next("/");
      }
    },
  },
  {
    path: "/theatres",
    name: "theatres-page",
    component: Theatres,
    beforeEnter: (to, from, next) => {
      if (isUserAlive()) {
        next();
      } else {
        next("/");
      }
    },
  },
  {
    path: "/selected-Movie/:movieId",
    name: "selected-Movie",
    component: SelectedMovie,
    beforeEnter: (to, from, next) => {
      if (isUserAlive()) {
        next();
      } else {
        next("/");
      }
    },
  },
  {
    path: "/selected-slot/:slotId",
    name: "selected-slot",
    component: SelectedSlot,
    beforeEnter: (to, from, next) => {
      if (isUserAlive()) {
        next();
      } else {
        next("/");
      }
    },
  },
  {
    path: "/selected-theatre/:theatreId",
    name: "selected-theatre",
    component: SelectedTheatre,
    beforeEnter: (to, from, next) => {
      if (isUserAlive()) {
        next();
      } else {
        next("/");
      }
    },
  },
  {
    path: "/booking/:slotId/:seatCount",
    name: "booking-page",
    component: Booking,
    beforeEnter: (to, from, next) => {
      if (isUserAlive()) {
        next();
      } else {
        next("/");
      }
    },
  },
  {
    path: "/profile",
    name: "profile-page",
    component: Profile,
    beforeEnter: (to, from, next) => {
      if (isUserAlive()) {
        next();
      } else {
        next("/");
      }
    },
  },
  {
    path: "/logout",
    name: "log-out",
    beforeEnter: (to, from, next) => {
      localStorage.clear();
      next("/");
    },
  },
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
