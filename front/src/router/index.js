import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
  {
    path: "/note",
    name: "Home",
    component: Home,
  },
  {
    path: "/note/new",
    name: "New",
    component: () => import("../views/New.vue"),
  },
  {
    path: "/note/:id",
    name: "List",
    component: () => import("../views/List.vue"),
  },
  {
    path: "/note/:id/edit",
    name: "Edit",
    component: () => import("../views/Edit.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
