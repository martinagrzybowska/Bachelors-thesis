<template>
	<div class="main-container">
		
		<sidebar></sidebar>

		<div class="container">
			
			<div class="header-container">
				<div class="current-heading">
					<p>Performance profiles comparison</p>
				</div>
				<div class="current-heading right">
					<p>repository <span>{{ this.$route.params.repo | capitalizeFirst }}</span></p>
				</div>
			</div>

			<div>
				<div class="two-col-table-header">
					<span @click="isBaselineTargetInfoActive = !isBaselineTargetInfoActive">Baseline profile</span>
					<span class="arrow" :class="isBaselineTargetInfoActive ? 'show' : 'hide'"></span>
				</div>
			</div>
			
			<div v-show="isBaselineTargetInfoActive" class="dashboard-repo-info-wrapper compare">
				
				<div class="dashboard-repo-info">
					<div>
						<span class="heading">Original performance profile:</span>
					</div>
					<div>
						<span @click="goTo('profile', baseline_commit, baseline_id)">{{ baseline_id }}</span>
					</div>
				</div>
				
				<div class="dashboard-repo-info">
					<div>
						<span class="heading">Belonging to minor version:</span>
					</div>
					<div>
						<span @click="goTo('commit', baseline_commit, '')">{{ baseline_commit }}</span>
					</div>
				</div>
				
				<div class="dashboard-repo-info">
					<div>
						<span class="heading">Found at path:</span>
					</div>
					<div>
						<span class="path">{{ baseline_path }}</span>
					</div>
				</div>

			</div>
			
			<profileChart 
				:chartData="profilesToCompare.baseline.resources" 
				:originalOptions="originalBaselineOptions" 
				:originalNumericalOptions="originalBaselineNumericalOptions" 
				:profileName="baseline_id">
			</profileChart>

			<div>
				<div class="two-col-table-header">
					<span @click="isTargetInfoActive = !isTargetInfoActive">Target profile</span>
					<span class="arrow" :class="isTargetInfoActive ? 'show' : 'hide'"></span>
				</div>
			</div>

			<div v-show="isTargetInfoActive" class="dashboard-repo-info-wrapper compare">
				
				<div class="dashboard-repo-info">
					<div>
						<span class="heading">Comparing to performance profile:</span>
					</div>
					<div>
						<span @click="goTo('profile', target_commit, target_id)">{{ target_id }}</span>
					</div>
				</div>
				
				<div class="dashboard-repo-info">
					<div>
						<span class="heading">Belonging to minor version:</span>
					</div>
					<div>
						<span @click="goTo('commit', target_commit, '')">{{ target_commit }}</span>
					</div>
				</div>
				
				<div class="dashboard-repo-info">
					<div>
						<span class="heading">Found at path:</span>
					</div>
					<div>
						<span class="path">{{ target_path }}</span>
					</div>
				</div>

			</div>

			<profileChart 
				:chartData="profilesToCompare.target.resources" 
				:originalOptions="originalTargetOptions" 
				:originalNumericalOptions="originalTargetNumericalOptions" 
				:profileName="target_id">
			</profileChart>
			
		</div>
	</div>
</template>

<script type="text/javascript">
	export default {
		data: function() {
			return {
				isBaselineTargetInfoActive: true,
				isTargetInfoActive: true,
				baseline_commit: this.$route.params.baseline_commit,
				baseline_id: this.$route.params.baseline_id,
				baseline_path: this.$route.params.baseline_path,
				target_commit: this.$route.params.target_commit,
				target_id: this.$route.params.target_id,
				target_path: this.$route.params.target_path,
			}
		},
		created: function() {
			this.$store.dispatch({
				type: 'getProfilesToCompare',
				baseline: {commit: this.$route.params.baseline_commit, id: this.$route.params.baseline_id, path: this.$route.params.baseline_path},
				target: {commit: this.$route.params.target_commit, id: this.$route.params.target_id, path: this.$route.params.target_path},
				path: this.originRepositoryPath,
			});
		},
		computed: {
			/**
			 * Gets current repository name from shared state
			 */
			originRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			},
			/**
			 * Gets profiles' data from the shared state
			 */
			profilesToCompare: function() {
				return this.$store.getters.compareProfiles;
			},
			/**
			 * Gets baseline profile original options from the shared state
			 */
			originalBaselineOptions: {
				get: function() {
					var output = this.profilesToCompare.baseline.chart_options;
					output.push('----');
					return output;
				},
				set: function() {
				}
			},
			/**
			 * Gets baseline profile original numerical options from the shared state
			 */
			originalBaselineNumericalOptions: {
				get: function() {
					var output = this.profilesToCompare.baseline.chart_numerical_options;
					output.push('----');
					return output;
				},
				set: function() {
				}
			},
			/**
			 * Gets target profile original options from the shared state
			 */
			originalTargetOptions: {
				get: function() {
					var output = this.profilesToCompare.target.chart_options;
					output.push('----');
					return output;
				},
				set: function() {
				}
			},
			/**
			 * Gets target profile original numerical options from the shared state
			 */
			originalTargetNumericalOptions: {
				get: function() {
					var output = this.profilesToCompare.target.chart_numerical_options;
					output.push('----');
					return output;
				},
				set: function() {
				}
			},
		},
		methods: {
			/**
			 * Switches context
			 */
			goTo: function(type, commit, profile) {
				if (type == 'commit')
					this.$router.push({ 
						name: 'commit',
						params: { 
							repo: this.$route.params.repo,
							commit: commit,
							originRepositoryPath: this.originRepositoryPath,
					}});
				else {
					this.$router.push({ 
						name: 'profile',
						params: { 
							repo: this.$route.params.repo, 
							commit: commit,
							profileId: profile,
							originRepositoryPath: this.originRepositoryPath,
						}});
				}
			}
		}
	}
</script>