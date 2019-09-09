import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";
import Login from "@/pages/Login.vue";

// Admin pages
const Dashboard = () => import(/* webpackChunkName: "dashboard" */"@/pages/Dashboard.vue");
const Profile = () => import(/* webpackChunkName: "common" */ "@/pages/Profile.vue");
// const Notifications = () => import(/* webpackChunkName: "common" */"@/pages/Notifications.vue");
const Icons = () => import(/* webpackChunkName: "common" */ "@/pages/Icons.vue");
// const Maps = () => import(/* webpackChunkName: "common" */ "@/pages/Maps.vue");
// const Typography = () => import(/* webpackChunkName: "common" */ "@/pages/Typography.vue");
// const TableList = () => import(/* webpackChunkName: "common" */ "@/pages/TableList.vue");
const Upload = () => import(/* webpackChunkName: "common" */ "@/pages/Upload.vue");

const routes = [
  {
    path: '/',
    name: 'start',
    component: Login,
  },
  {
    path: '/main',
    name: 'home',
    component: DashboardLayout,
    children: [
      {
        path: "dashboard",
        name: "dashboard",
        component: Dashboard
      }, 
      {
        path: "profile",
        name: "profile",
        component: Profile
      },
      {
        path: "icons",
        name: "icons",
        component: Icons
      },
      {
        path: "upload",
        name: "upload",
        component: Upload
      },      
    ]
  },
  { path: "*", component: NotFound }
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;
