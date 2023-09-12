import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import CreateAdmin from "./components/admin/CreateAdmin";
import CreateShow from "./components/admin/CreateShow";
import CreateVenue from "./components/admin/CreateVenue";
import UpdateShow from "./components/admin/UpdateShow";
import UpdateVenue from "./components/admin/UpdateVenue";
import DeleteShow from "./components/admin/DeleteShow";
import DeleteVenue from "./components/admin/DeleteVenue";
import Shows from "./components/user/Shows";
import Venues from "./components/user/Venues";
import SelectedShow from "./components/user/SelectedShow";
import SelectedVenue from "./components/user/SelectedVenue";
import SelectedSlot from "./components/user/SelectedSlot";
import Booking from "./components/user/Booking";
import Profile from "./components/user/Profile";

const routes = [
  {
    path: "/",
    name: "log-in",
    component: Login,
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
  },
  {
    path: "/add-show",
    name: "create-show",
    component: CreateShow,
  },
  {
    path: "/add-venue",
    name: "create-venue",
    component: CreateVenue,
  },
  {
    path: "/update-show",
    name: "update-show",
    component: UpdateShow,
  },
  {
    path: "/update-venue",
    name: "update-venue",
    component: UpdateVenue,
  },
  {
    path: "/delete-show",
    name: "Delete-show",
    component: DeleteShow,
  },
  {
    path: "/delete-venue",
    name: "delete-venue",
    component: DeleteVenue,
  },
  {
    path: "/shows",
    name: "shows-page",
    component: Shows,
  },
  {
    path: "/venues",
    name: "venues-page",
    component: Venues,
  },
  {
    path: "/selected-show",
    name: "selected-show",
    component: SelectedShow,
  },
  {
    path: "/selected-slot",
    name: "selected-slot",
    component: SelectedSlot,
  },
  {
    path: "/selected-venue",
    name: "selected-venue",
    component: SelectedVenue,
  },
  {
    path: "/booking",
    name: "booking-page",
    component: Booking,
  },
  {
    path: "/profile",
    name: "profile-page",
    component: Profile,
  },
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
