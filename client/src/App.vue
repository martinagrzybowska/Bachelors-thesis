<template>
	<div id="app">

		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
		 
		<div class="page-container">
			
			<transition name="fade">
				<successModal v-show="showSuccess"><div slot="header">Operation was successfull</div></successModal>
			</transition>
			
			<transition name="fade">
				<loadingModal v-show="showLoader"></loadingModal>
			</transition>
			
			<transition name="fade">
				<errorModal v-show="showError"><span slot="header">Oops, operation was unsuccessfull, try again</span></errorModal>
			</transition>

			<div class="navbar">
				
				<div class="navbar-left">
					<img src="./assets/perun-logo.png" class="logo" @click="goTo(''); isActive = 'repos'"/>
					<span>Perun: Performance Under Control</span>
				</div>
				
				<div class="navbar-right">
					<div @click="goTo(''); isActive = 'repos'" :class="isActive == 'repos' ? 'active' : ''"> 
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M488 128H24c-13.255 0-24-10.745-24-24V56c0-13.255 10.745-24 24-24h464c13.255 0 24 10.745 24 24v48c0 13.255-10.745 24-24 24zm-8 328V184c0-13.255-10.745-24-24-24H56c-13.255 0-24 10.745-24 24v272c0 13.255 10.745 24 24 24h400c13.255 0 24-10.745 24-24zM308 256H204c-6.627 0-12-5.373-12-12v-8c0-6.627 5.373-12 12-12h104c6.627 0 12 5.373 12 12v8c0 6.627-5.373 12-12 12z"/></svg>
						<span>Version Control Systems</span>
					</div>
					<div @click="goTo('global-settings'); isActive = 'global-settings'" :class="isActive == 'global-settings' ? 'active' : ''">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M364.215 192h131.43c5.439 20.419 8.354 41.868 8.354 64s-2.915 43.581-8.354 64h-131.43c5.154-43.049 4.939-86.746 0-128zM185.214 352c10.678 53.68 33.173 112.514 70.125 151.992.221.001.44.008.661.008s.44-.008.661-.008c37.012-39.543 59.467-98.414 70.125-151.992H185.214zm174.13-192h125.385C452.802 84.024 384.128 27.305 300.95 12.075c30.238 43.12 48.821 96.332 58.394 147.925zm-27.35 32H180.006c-5.339 41.914-5.345 86.037 0 128h151.989c5.339-41.915 5.345-86.037-.001-128zM152.656 352H27.271c31.926 75.976 100.6 132.695 183.778 147.925-30.246-43.136-48.823-96.35-58.393-147.925zm206.688 0c-9.575 51.605-28.163 104.814-58.394 147.925 83.178-15.23 151.852-71.949 183.778-147.925H359.344zm-32.558-192c-10.678-53.68-33.174-112.514-70.125-151.992-.221 0-.44-.008-.661-.008s-.44.008-.661.008C218.327 47.551 195.872 106.422 185.214 160h141.572zM16.355 192C10.915 212.419 8 233.868 8 256s2.915 43.581 8.355 64h131.43c-4.939-41.254-5.154-84.951 0-128H16.355zm136.301-32c9.575-51.602 28.161-104.81 58.394-147.925C127.872 27.305 59.198 84.024 27.271 160h125.385z"/></svg>
						<span>Global Settings</span>
					</div>
				</div>

			</div>

			<router-view></router-view>
			
		</div>
	</div>
</template>

<script>
export default {
	data () {
		return {
			isActive: 'repos',
		}
	},
	computed: {
		/**
		 * Shows loading screen modal
		 */
		showLoader: function() {
			return this.$store.getters.loadingScreen;
		},
		/**
		 * Shows success modal
		 */
		showSuccess: function() {
			return this.$store.getters.successScreen;
		},
		/**
		 * Shows error modal
		 */
		showError: function() {
			return this.$store.getters.errorScreen;
		},
	},
	methods: {
		/**
		 * Switches context to another location and fires action to reset current branch
		 * @param {string} destination to go to
		 */
		goTo: function(destination) {
			if (destination == '') {
				this.$store.dispatch('clearDashboard');
			}

			this.$store.dispatch('resetCurrentBranch');
			this.$router.push('/' + destination);
		}
	},
}
</script>

<style>
	@import 'assets/style.css'
</style>
