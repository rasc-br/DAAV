import Vue from "vue";
import VueRouter from "vue-router";
import RouterPrefetch from 'vue-router-prefetch'
import App from "./App";
// TIP: change to import router from "./router/starterRouter"; to start with a clean layout
import router from "./router/index";
// import router from "./router/starterRouter";

import BlackDashboard from "./plugins/blackDashboard";
import i18n from "./i18n"
import './registerServiceWorker'
Vue.use(BlackDashboard);
Vue.use(VueRouter);
Vue.use(RouterPrefetch);

let globalData = new Vue({
  data: { 
    $userProfileData: {
      email: 'songoku@universe7.com',
      username: 'sonGokuu',
      firstname: 'Son',
      lastname: 'Goku',
      address: 'Grandpa Gohan House',
      city: 'Mount Paozu',
      country: 'Universe 7',
      about: 'Osu, ora Gokuu',
      postalcode: '7777-777',
      avatar: 'img/goku.jpg',
      type: 'Simple User',
      imgtype: 'image/jpg'
    },
   }
});

Vue.mixin({
  // Global mixin, everything in here will be available to all components
  computed: {
    $userProfileData: {
      get: function () { return globalData.$data.$userProfileData },
      set: function (newUserProfileData) { globalData.$data.$userProfileData = newUserProfileData; }
    },    
  }
})

/* eslint-disable no-new */
new Vue({
  router,
  i18n,
  render: h => h(App)
}).$mount("#app");
