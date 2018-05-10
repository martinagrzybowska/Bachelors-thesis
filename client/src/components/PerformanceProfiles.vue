<template>
	<div class="main-container">

		<sidebar></sidebar>

		<div class="container">
			<div class="header-container">
				<div class="current-heading">
					<p>Performance Profiles</p>
				</div>
				<div class="current-heading right">
					<p>repository <span>{{ this.$route.params.repo | capitalizeFirst }}</span></p>
				</div>
			</div>
			
			<profilesToggle></profilesToggle>

		</div>
	
	</div>
</template>

<script type="text/javascript">
	export default {
		computed: {
			/**
			 * Gets current repository path from shared state
			 */
			originRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			}
		}
	}
</script>