<template>
	<div class="main-container">

		<sidebar></sidebar>

		<div class="container">
			<div class="header-container">
				<div class="current-heading">
					<p>Local Settings</p>
				</div>
				<div class="current-heading right">
					<p>repository <span>{{ this.$route.params.repo | capitalizeFirst }}</span></p>
				</div>
			</div>

			<div class="content-container">
				<div class="settings-sub-menu">
					
					<div class="settings-sub-menu-item" 
						v-for="item in submenuItems" 
						:key="item" @click="activeItem = item" 
						:class="activeItem == item ? 'active' : ''">
						
						<span>{{ item }}</span>
					
					</div>

				</div>

				<div class="settings-container">

					<settingsItems v-if="activeItem == 'General'" 
						:pagingOptions="pagingOptions" 
						:settings="settings.general" 
						type="general">
					</settingsItems>
					
					<settingsItems v-if="activeItem == 'Format'" 
						:settings="settings.format" 
						type="format">
					</settingsItems>

					<settingsItems v-if="activeItem == 'VCS'" 
						:settings="settings.vcs" 
						type="vcs">
					</settingsItems>

					<collectionSettings v-if="activeItem == 'Job Matrix'" 
						mode="job-matrix" 
						type="jobMatrix">
					</collectionSettings>

				</div>
			</div>
		</div>
	</div>
</template>

<script type="text/javascript">
	export default {
		data: function() {
			return {
				submenuItems: [
					'General', 'Format', 'VCS', 'Job Matrix'
				],
				activeItem: 'General',

				pagingOptions: [
					'always', 'only-log', 'only-status', 'never'
				],
			}
		},
		created: function() {
			this.$store.dispatch({
				type: 'loadLocalSettings',
				path: this.originRepositoryPath,
			});
		},
		computed: {
			/**
			 * Gets current repository path from shared state
			 */
			originRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			},
			/**
			 * Gets copy of local settings from the shared state
			 */
			settings: function() {
				return this.$store.getters.localSettings;
			}
		}
	}
</script>









