import { createRouter, createWebHashHistory } from "vue-router";
import Login from "../views/Login.vue";
import About from "../views/About.vue";
import Lost from "../views/Lost.vue";
import Found from "../views/Found.vue";
import RegisterLost from "../views/Register-Lost.vue";
import RegisterFound from "../views/Register-Found.vue";
import User from "../views/User.vue";
import UserProfile from "../views/UserProfile.vue";
import Chats from "../views/Chats.vue";
import ListItem from "../views/ListItem.vue";
import UserItemsLost from "../views/UserItems-Lost.vue";
import UserItemsFound from "../views/UserItems-Found.vue";
import Message from "../views/Message.vue";
import SessionExpired from "@/views/Session-Expired.vue";
import api from "../services/api";
import Anonimo from "@/views/Anonimo.vue";
import EditItem from "../views/EditItem.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/about",
    name: "About",
    component: About,
    meta: { requiresAuth: true },
  },
  {
    path: "/lost",
    name: "Lost",
    component: Lost,
    meta: { requiresAuth: true },
  },
  {
    path: "/found",
    name: "Found",
    component: Found,
    meta: { requiresAuth: true },
  },
  {
    path: "/register-lost",
    name: "RegisterLost",
    component: RegisterLost,
    meta: { requiresAuth: true },
  },
  {
    path: "/register-found",
    name: "RegisterFound",
    component: RegisterFound,
    meta: { requiresAuth: true },
  },
  {
    path: "/edit-item/:id",
    name: "EditItem",
    component: EditItem,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: "/user",
    name: "User",
    component: User,
    meta: { requiresAuth: true },
  },
  {
    path: "/user-profile/:id",
    name: "UserProfile",
    component: UserProfile,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: "/chats",
    name: "Chats",
    component: Chats,
    meta: { requiresAuth: true },
  },
  {
    path: "/list-item",
    name: "ListItem",
    component: ListItem,
    meta: { requiresAuth: true },
  },
  {
    path: "/user-items-lost",
    name: "UserItemsLost",
    component: UserItemsLost,
    meta: { requiresAuth: true },
  },
  {
    path: "/user-items-found",
    name: "UserItemsFound",
    component: UserItemsFound,
    meta: { requiresAuth: true },
  },
  {
    path: "/chat/new",
    name: "NewChat",
    component: Message,
    meta: { requiresAuth: true },
  },
  {
    path: "/chat/:chatroomId/:itemId?",
    name: "Chat",
    component: Message,
    meta: { requiresAuth: true },
    props: (route) => ({
      chatroomId: route.params.chatroomId || route.query.chatroomId,
      itemId: route.params.itemId || route.query.itemId,
    }),
  },
  {
    path: "/anonimo",
    name: "Anonimo",
    component: Anonimo,
  },
  {
    path: "/session-expired",
    name: "Expired",
    component: SessionExpired,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach(async (to) => {
  if (to.meta.requiresAuth) {
    try {
      await api.get("/auth/validate", {
        withCredentials: true,
      });
      return true;
    } catch {
      return { name: "Expired" };
    }
  }
  return true;
});

export default router;
