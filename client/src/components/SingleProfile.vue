<template>
	<div class="main-container">

		<sidebar></sidebar>
		
		<transition name="fade">
			<postprocessModal 
				v-show="isPostprocessModalVisible" 
				@close="closeModal('postprocess')" 
				:realpath="profileInfo.profiled_command[0].path" 
				:registered="profileInfo.registered">
			</postprocessModal>
		</transition>

		<transition name="fade">
			<removeModal 
				v-show="isConfirmModalVisible" 
				@close="closeModal('confirm')" 
				@confirm="unregisterProfile()">
					<span slot="header">Do you really wish to remove the performance profile <b>{{ this.$route.params.profileId }}</b>?</span>
			</removeModal>
		</transition>
		
		<div class="container">
			
			<div class="header-container">
				<div class="current-heading">
					<p>Performance profile {{ this.$route.params.profileId }}</p>
				</div>
				<div class="current-heading right">
					<p>repository <span>{{ this.$route.params.repo | capitalizeFirst }}</span></p>
				</div>
			</div>

			<div class="profile-info-container">
				<div class="profile-origin">
					
					<div>
						<span>Original minor version is </span>
						<span class="point" @click="goTo()"><b>{{ this.$route.params.commit }}</b></span>
					</div>
					
					<div class="profile-origin-buttons">
						
						<div class="table-button" :class="profileInfo.registered ? 'register' : 'unregister'">
							<span>{{profileInfo.registered ? 'registered' : 'pending'}}</span>
							<svg v-if="profileInfo.registered"xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z"/></svg>
							<svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm61.8-104.4l-84.9-61.7c-3.1-2.3-4.9-5.9-4.9-9.7V116c0-6.6 5.4-12 12-12h32c6.6 0 12 5.4 12 12v141.7l66.8 48.6c5.4 3.9 6.5 11.4 2.6 16.8L334.6 349c-3.9 5.3-11.4 6.5-16.8 2.6z"/></svg>
						</div>
						
						<div class="table-button" :class="profileInfo.registered ? 'remove' : ''" @click="toggleRegistration()">
							<span>{{!profileInfo.registered ? 'register' : 'remove'}}</span>
							<svg v-if="profileInfo.registered" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
							<svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z"/></svg>
						</div>

					</div>
				</div>

				<div>
					
					<div class="two-col-table-header" :class="isActive.profiled_command ? '' : 'bottom-border'">
						<span @click="isActive.profiled_command = !isActive.profiled_command">Profiled commmand</span>
						<span class="arrow" :class="isActive.profiled_command ? 'show' : 'hide'"></span>
					</div>
					
					<div class="two-col-table" v-if="isActive.profiled_command">
						<div class="two-col-item" v-for="(row, index) in profileInfo.profiled_command" :key="'profiled' + index">
							<template v-for="(value, key) in row">
								<span :key="'key' + key" >{{ key | capitalizeFirst }}:</span>
								<span :key="'value' + key">{{ value }}</span>
							</template>
						</div>
					</div>

				</div>
				
				<div>
					
					<div class="two-col-table-header" :class="isActive.collection_configuration ? '' : 'bottom-border'">
						<span @click="isActive.collection_configuration = !isActive.collection_configuration">Collection configuration</span>
						<span class="arrow" :class="isActive.collection_configuration ? 'show' : 'hide'"></span>
					</div>
					
					<div class="two-col-table" v-if="isActive.collection_configuration">
						<div class="two-col-item" v-for="(row, index) in profileInfo.collection_configuration"
							:key="'coll' + index"
							:class="row['postprocessors'] ? 'postprocessors' : ''">
							
							<template v-for="(value, key) in row">
								
								<template v-if="key != 'postprocessors'">
									<span :key="'coll' + index + 'key'">{{ key | capitalizeFirst }}:</span>
									<span :key="'coll' + index + 'value'">{{ value }}</span>
								</template>
								
								<template v-else>
									
									<div :key="'post' + index + 'key'">
										<span>{{ key | capitalizeFirst }}:</span>
										<template v-for="(item, index) in value">
											<span :key="'opt' + index" >{{ item }}</span>
											<span :key="'optcomma' + index" v-if="index < (value.length - 1)">, </span>
										</template>
									</div>
									
									<div :key="'post' + index + 'value'" class="table-button reload" @click="showModal('postprocess')">
										<span>postprocess</span>
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512.333 512"><path d="M440.935 12.574l3.966 82.766C399.416 41.904 331.674 8 256 8 134.813 8 33.933 94.924 12.296 209.824 10.908 217.193 16.604 224 24.103 224h49.084c5.57 0 10.377-3.842 11.676-9.259C103.407 137.408 172.931 80 256 80c60.893 0 114.512 30.856 146.104 77.801l-101.53-4.865c-6.845-.328-12.574 5.133-12.574 11.986v47.411c0 6.627 5.373 12 12 12h200.333c6.627 0 12-5.373 12-12V12c0-6.627-5.373-12-12-12h-47.411c-6.853 0-12.315 5.729-11.987 12.574zM256 432c-60.895 0-114.517-30.858-146.109-77.805l101.868 4.871c6.845.327 12.573-5.134 12.573-11.986v-47.412c0-6.627-5.373-12-12-12H12c-6.627 0-12 5.373-12 12V500c0 6.627 5.373 12 12 12h47.385c6.863 0 12.328-5.745 11.985-12.599l-4.129-82.575C112.725 470.166 180.405 504 256 504c121.187 0 222.067-86.924 243.704-201.824 1.388-7.369-4.308-14.176-11.807-14.176h-49.084c-5.57 0-10.377 3.842-11.676 9.259C408.593 374.592 339.069 432 256 432z"/></svg>
									</div>

								</template>

							</template>
						</div>
					</div>
				</div>

				<div>
					
					<div class="two-col-table-header" :class="isActive.visualization ? '' : 'bottom-border'">
						<span @click="isActive.visualization = !isActive.visualization">Visualization</span>
						<span class="arrow" :class="isActive.visualization ? 'show' : 'hide'"></span>
					</div>
					
					<div v-if="isActive.visualization">
						<profileChart 
							:chartData="profileInfo.resources" 
							:originalOptions="originalOptions" 
							:originalNumericalOptions="originalNumericalOptions">
						</profileChart>
					</div>
			
				</div>
				
				
				<div class="comparation">
					<div class="two-col-table-header bottom-border">
						<span>Profile comparison</span>
					</div>
					
					<div v-if="isActive.comparation">
						
						<div class="table-button reload compare" @click="getOptions()">
							<span>{{showComparationOptions ? 'hide options' : 'show options'}}</span>
							<svg v-if="!showComparationOptions"xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M504 256c0 137-111 248-248 248S8 393 8 256 119 8 256 8s248 111 248 248zM273 369.9l135.5-135.5c9.4-9.4 9.4-24.6 0-33.9l-17-17c-9.4-9.4-24.6-9.4-33.9 0L256 285.1 154.4 183.5c-9.4-9.4-24.6-9.4-33.9 0l-17 17c-9.4 9.4-9.4 24.6 0 33.9L239 369.9c9.4 9.4 24.6 9.4 34 0z"/></svg>
							<svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M8 256C8 119 119 8 256 8s248 111 248 248-111 248-248 248S8 393 8 256zm231-113.9L103.5 277.6c-9.4 9.4-9.4 24.6 0 33.9l17 17c9.4 9.4 24.6 9.4 33.9 0L256 226.9l101.6 101.6c9.4 9.4 24.6 9.4 33.9 0l17-17c9.4-9.4 9.4-24.6 0-33.9L273 142.1c-9.4-9.4-24.6-9.4-34 0z"/></svg>
						</div>
						
						<transition name="fade">
							<div v-show="showComparationOptions" class="two-col-table">
								<div class="two-col-item">
									
									<div>
										<span>Compare current profile with</span>
									</div>
									
									<div class="compare-profiles-input">
										
										<select v-model="selectedProfileCompare" class="selectpicker">
											<option v-for="profile in profilesList" :value="profile" :key="profile.id">{{ profile.id }}</option>
										</select>
										
										<div class="table-button compare" @click="goToCompareProfiles()">
											<span>compare both</span>
											<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M569.354 231.631C512.969 135.949 407.81 72 288 72 168.14 72 63.004 135.994 6.646 231.631a47.999 47.999 0 0 0 0 48.739C63.031 376.051 168.19 440 288 440c119.86 0 224.996-63.994 281.354-159.631a47.997 47.997 0 0 0 0-48.738zM288 392c-75.162 0-136-60.827-136-136 0-75.162 60.826-136 136-136 75.162 0 136 60.826 136 136 0 75.162-60.826 136-136 136zm104-136c0 57.438-46.562 104-104 104s-104-46.562-104-104c0-17.708 4.431-34.379 12.236-48.973l-.001.032c0 23.651 19.173 42.823 42.824 42.823s42.824-19.173 42.824-42.823c0-23.651-19.173-42.824-42.824-42.824l-.032.001C253.621 156.431 270.292 152 288 152c57.438 0 104 46.562 104 104z"/></svg>
										</div>

									</div>

								</div>
							</div>
						</transition>

					</div>
				</div>


			</div>
		</div>
	</div>
</template>

<script type="text/javascript">
	import PostprocessModal from './PostprocessModal.vue'
	
	export default {
		components: {
			'postprocessModal' : PostprocessModal,
		},
		data: function() {
			return {
				isActive: {
					profiled_command: true,
					collection_configuration: true,
					visualization: true,
					comparation: true,
				},
				showComparationOptions: false,
				selectedProfileCompare: '',
				isPostprocessModalVisible: false,
				isConfirmModalVisible: false,
				first: true,
			}
		},
		created: function() {
			this.$store.dispatch({
				type: 'loadProfile',
				path: this.originRepositoryPath,
				commitId: this.$route.params.commit,
				profileId: this.$route.params.profileId,
			});
			this.$store.dispatch({
				type: 'getCompareProfilesList',
				id: this.$route.params.profileId,
				path: this.originRepositoryPath,
			})
		},
		computed: {
			originRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			},
			profilesList: function() {
				return this.$store.getters.compareProfilesList;
			},
			profileInfo: function() {
				return this.$store.getters.profile;
			},
			originalOptions: {
				get: function() {
					var output = this.$store.getters.profile.chart_options;
					output.push('----');
					return output;
				},
				set: function() {
				}
			},
			originalNumericalOptions: {
				get: function() {
					var output = this.$store.getters.profile.chart_numerical_options;
					output.push('----');
					return output;
				},
				set: function() {
				}
			},
		},
		methods: {
			/**
			 * Toggles visibility of options panel
			 */
			getOptions: function() {
				this.showComparationOptions = !this.showComparationOptions;
			},
			/**
			 * Fires action to get data of profiles which are to be compared
			 */
			goToCompareProfiles: function() {
				this.$router.push({ 
					name: 'profiles-comparation',
					params: { 
						repo: this.$route.params.repo,
						baseline_commit: this.$route.params.commit,
						baseline_id: this.$route.params.profileId,
						baseline_path: this.profileInfo.profiled_command[0].path,
						target_commit: this.selectedProfileCompare.commit,
						target_id: this.selectedProfileCompare.id,
						target_path: this.selectedProfileCompare.path,
					}
				});
			},
			/**
			 * Shows modal window depending on type
			 * @param {string} type of modal window to show, eg. prostprocess or confirm
			 */
			showModal: function(type) {
	    		if (type == 'postprocess') {
	    			this.isPostprocessModalVisible = true;
	    		}
	    		else if (type == 'confirm') {
	    			this.isConfirmModalVisible = true;
	    		}
	    	},
	    	/**
			 * Hides modal window depending on type
			 * @param {string} type of modal window to hide, eg. prostprocess or confirm
			 */
	    	closeModal: function(type) {
	    		if (type == 'postprocess') {
	    			this.isPostprocessModalVisible = false;
	    		}
	    		else if (type == 'confirm') {
	    			this.isConfirmModalVisible = false;
	    		}
	    	},
	    	/**
			 * Toggles registration of a profile
			 */
			toggleRegistration: function() {
				if (this.profileInfo.registered) {
					this.showModal('confirm');
				}
				else {
					this.registerProfile();
				}
			},
			/**
			 * Fires action which registeres a profile
			 */
			registerProfile: function() {
				this.$store.dispatch({
					type: 'registerProfile',
					profileId: this.$route.params.profileId,
					profilePath: this.profileInfo.profiled_command[0].path,
					commitId: this.$route.params.commit,
					path: this.originRepositoryPath,
				})
			},
			/**
			 * Fires action which unregisteres a profile
			 */
			unregisterProfile: function() {
				this.$store.dispatch({
					type: 'unregisterProfile',
					profileId: this.$route.params.profileId,
					commitId: this.$route.params.commit,
					path: this.originRepositoryPath,
				})
				this.closeModal('confirm');
				this.$router.go(-1);
			},
			/**
			 * Switches context to another commit
			 */
			goTo: function() {
				this.$router.push({ 
					name: 'commit',
					params: { 
						repo: this.$route.params.repo,
						commit: this.$route.params.commit,
						originRepositoryPath: this.originRepositoryPath,
				}});
			}
		}
	}
</script>
