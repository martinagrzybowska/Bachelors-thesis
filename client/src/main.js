import lodash from 'lodash'
import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import { store } from './store/store'
import Loader from 'vue-spinner/src/RiseLoader.vue'
// import createPersistedState from 'vuex-persistedstate'
import VueHighcharts from 'vue-highcharts'



import Repos from './components/Repos.vue'
import GlobalSettings from './components/GlobalSettings.vue'
import NotFound from './components/NotFound.vue'

import Sidebar from './components/Sidebar.vue'
import Dashboard from './components/Dashboard.vue'

import AllCommits from './components/AllCommits.vue'
import SingleCommit from './components/SingleCommit.vue'
import PerformanceProfiles from './components/PerformanceProfiles.vue'
import ProfilesToggle from './components/ProfilesToggle.vue'
import ProfileTable from './components/ProfileTable.vue'
import SingleProfile from './components/SingleProfile.vue'
import ProfileChart from './components/ProfileChart'
import ProfilesCompare from './components/ProfilesCompare'
import TwoColTables from './components/TwoColTables.vue'

import LocalSettings from './components/LocalSettings.vue'
import SettingsItems from './components/SettingsItems.vue'
import CollectionSettings from './components/CollectionSettings.vue'

import Modal from './components/Modal.vue'
import ErrorModal from './components/ErrorModal.vue'
import SuccessModal from './components/SuccessModal.vue'
import RemoveModal from './components/RemoveModal.vue'
import LoadingModal from './components/LoadingModal.vue'
import SmilingCookie from './components/SmilingCookie.vue'

Vue.use(VueRouter);
Vue.use(VueHighcharts);

Vue.component('repos', Repos);
Vue.component('globalSettings', GlobalSettings);
Vue.component('notFound', NotFound);

Vue.component('sidebar', Sidebar);
Vue.component('dashboard', Dashboard);

Vue.component('allCommits', AllCommits);
Vue.component('singleCommit', SingleCommit);
Vue.component('performanceProfiles', PerformanceProfiles);
Vue.component('singleProfile', SingleProfile);
Vue.component('profilesToggle', ProfilesToggle);
Vue.component('profileTable', ProfileTable);
Vue.component('twoColTables', TwoColTables);
Vue.component('profileChart', ProfileChart);
Vue.component('profilesCompare', ProfilesCompare);

Vue.component('localSettings', LocalSettings);
Vue.component('settingsItems', SettingsItems);
Vue.component('collectionSettings', CollectionSettings);

Vue.component('mmodal', Modal);
Vue.component('successModal', SuccessModal);
Vue.component('removeModal', RemoveModal);
Vue.component('errorModal', ErrorModal)
Vue.component('Loader', Loader);
Vue.component('loadingModal', LoadingModal)
Vue.component('smilingCookie', SmilingCookie)

const routes = [
	{ path: '/', component: Repos },
	{ path: '/global-settings', component: GlobalSettings },
	{ path: '/:repo/dashboard', name:'dashboard', component: Dashboard, props: true },
	{ path: '/:repo/minor-versions', name:'minor-versions', component: AllCommits, props: true },
	{ path: '/:repo/minor-versions/:commit', name:'commit', component: SingleCommit, props: true },
	{ path: '/:repo/performance-profiles', name:'performance-profiles', component: PerformanceProfiles, props: true },
	{ path: '/:repo/performance-profiles/:commit/:profileId', name:'profile', component: SingleProfile, props: true },
	{ path: '/:repo/local-settings', name:'local-settings', component: LocalSettings, props: true },
	{ path: '/:repo/performance-profiles/profiles-comparation', name:'profiles-comparation', component: ProfilesCompare, props: true },
	{ path: '*', component: NotFound }
]

const router = new VueRouter({
	routes: routes,
	// mode: 'history',
	scrollBehavior (to, from, savedPosition) {
		return { x: 0, y: 0 }
	},
})

Vue.filter('capitalizeFirst', function (string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
})

new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App)
})
