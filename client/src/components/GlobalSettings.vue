<template>
	<div class="main-container">

		<div class="container">
				
			<div class="header-container">
				<div class="current-heading">
					<p>Global Settings</p>
				</div>
			</div>
			
			<div class="content-container">

				<div class="settings-sub-menu">
					<div class="settings-sub-menu-item" v-for="item in submenuItems" 
						@click="activeItem = item" 
						:class="activeItem == item ? 'active' : ''">
						
						<span>{{ item }}</span>

					</div>
				</div>
				<div class="settings-container">
					
					<settingsItems v-if="activeItem == 'General'" 
						:settings="settings.general" 
						:pagingOptions="pagingOptions" 
						type="general" 
						mode="global">
					</settingsItems>
					
					<settingsItems v-if="activeItem == 'Format'" 
						:settings="settings.format" 
						type="format" 
						mode="global">
					</settingsItems>

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
					'General', 'Format'
				],
				activeItem: 'General',

				pagingOptions: [
					'always', 'only-log', 'only-status', 'never'
				],
			}
		},
		created: function() {
			this.$store.dispatch('loadGlobalSettings');
		},
		computed: {
			/**
			 * Gets global settings from the shared state
			 */
			settings: function() {
				return this.$store.getters.globalSettings;
			}
		}
	}
</script>