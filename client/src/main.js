import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// import jQuery from 'jquery';
// window.$ = window.jQuery = jQuery;

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.js'
createApp(App).use(router).mount('#app');
