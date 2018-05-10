<template>
	<transition name="custom-modal-fade">
		<div class="custom-modal-backdrop postprocess" @click.self="close()">
			<div class="custom-modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
				
				<div class="custom-modal-header" id="modalTitle">
					<div><slot name="header">Profile postprocessing specification</slot></div>
					<svg @click="close" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
				</div>
				
				<div class="custom-modal-body" id="modalDescription">
				
					<div class="settings-item job-matrix">
						<div>
							<span class="settings-item-heading">Postprocessor</span>
							<span class="settings-item-subheading">Specification of the postprocessing unit and its configuration</span>
						</div>

						<div class="collection-specification-container commands-item">
							<div>
								<div class="collection-specification">

									<span class="settings-item-heading secondary">Name</span>
									
									<div class="settings-item-input-container collection-specification">
										<input type="text" class="search-bar" placeholder="eg. regression analysis" v-model="postprocessor.name">
									</div>

									<div class="collection-specification-params">
										<div class="parameters">
											<span class="settings-item-heading secondary">Parameters</span>
										</div>
										<div class="values">
											<span class="settings-item-heading secondary">Values</span>
										</div>
									</div>
									
									<div v-if="postprocessor.parameters.length == 0" class="settings-item-input-add" @click="addParam(type,itemIndex)">
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M448 294.2v-76.4c0-13.3-10.7-24-24-24H286.2V56c0-13.3-10.7-24-24-24h-76.4c-13.3 0-24 10.7-24 24v137.8H24c-13.3 0-24 10.7-24 24v76.4c0 13.3 10.7 24 24 24h137.8V456c0 13.3 10.7 24 24 24h76.4c13.3 0 24-10.7 24-24V318.2H424c13.3 0 24-10.7 24-24z"/></svg>
									</div>
									
									<div class="collection-specification-params" v-for="(param, paramIndex) in postprocessor.parameters" :key="'param' + paramIndex">
										
										<div class="parameters">
											<div>
												<input type="text" class="search-bar" v-model="param.param" placeholder="eg. regression models">
												<div class="settings-item-input-add" @click="deleteParam(paramIndex)">
													<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M0 84V56c0-13.3 10.7-24 24-24h112l9.4-18.7c4-8.2 12.3-13.3 21.4-13.3h114.3c9.1 0 17.4 5.1 21.5 13.3L312 32h112c13.3 0 24 10.7 24 24v28c0 6.6-5.4 12-12 12H12C5.4 96 0 90.6 0 84zm416 56v324c0 26.5-21.5 48-48 48H80c-26.5 0-48-21.5-48-48V140c0-6.6 5.4-12 12-12h360c6.6 0 12 5.4 12 12zm-272 68c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208z"/></svg>
												</div>
												<span class="secondary">:</span>
											</div>
											<div v-if="(paramIndex + 1) == postprocessor.parameters.length" class="settings-item-input-add" @click="addParam()">
												<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M448 294.2v-76.4c0-13.3-10.7-24-24-24H286.2V56c0-13.3-10.7-24-24-24h-76.4c-13.3 0-24 10.7-24 24v137.8H24c-13.3 0-24 10.7-24 24v76.4c0 13.3 10.7 24 24 24h137.8V456c0 13.3 10.7 24 24 24h76.4c13.3 0 24-10.7 24-24V318.2H424c13.3 0 24-10.7 24-24z"/></svg>
											</div>
										</div>
										
										<div class="values">
											<div class="value-inputs-container">
												
												<template v-for="(option, optionIndex) in param.options">
													<input type="text" class="search-bar" v-model="param.options[optionIndex]" placeholder="eg. linear" :key="'input' + optionIndex">
													<div class="settings-item-input-add"  @click="deleteParamOption(paramIndex,optionIndex)" :key="'button' + optionIndex">
														<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M0 84V56c0-13.3 10.7-24 24-24h112l9.4-18.7c4-8.2 12.3-13.3 21.4-13.3h114.3c9.1 0 17.4 5.1 21.5 13.3L312 32h112c13.3 0 24 10.7 24 24v28c0 6.6-5.4 12-12 12H12C5.4 96 0 90.6 0 84zm416 56v324c0 26.5-21.5 48-48 48H80c-26.5 0-48-21.5-48-48V140c0-6.6 5.4-12 12-12h360c6.6 0 12 5.4 12 12zm-272 68c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208z"/></svg>
													</div>
												</template>

												<div class="settings-item-input-add" @click="addParamOption(paramIndex)">
													<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M448 294.2v-76.4c0-13.3-10.7-24-24-24H286.2V56c0-13.3-10.7-24-24-24h-76.4c-13.3 0-24 10.7-24 24v137.8H24c-13.3 0-24 10.7-24 24v76.4c0 13.3 10.7 24 24 24h137.8V456c0 13.3 10.7 24 24 24h76.4c13.3 0 24-10.7 24-24V318.2H424c13.3 0 24-10.7 24-24z"/></svg>
												</div>

											</div>
										</div>

									</div>

								</div>
							</div>

							<div class="settings-item-input-add"></div>

						</div>
					</div>


				</div>

					
				<div class="custom-modal-footer">
					<div class="table-button" @click="postprocessProfile()">
						<span>process</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z"/></svg>
					</div>
					<div class="table-button remove" @click="close">
						<span>cancel</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
					</div>
				</div>

			</div>
		</div>
	</transition>
</template>

<script type="text/javascript">
	export default {
		props: {
			realpath: {
				type: String,
				required: true,
			},
			registered: {
				type: Boolean,
				required: true,
			},
		},
		data: function() {
			return {
				postprocessor: { 
					name: '', 
					parameters: [
						{ param: '', options: [''] } 
					] 
				},
			}
		},
		computed: {
			/**
			 * Gets current repository path from shared state
			 */
			originalRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			},
		},
		methods: {
			/**
			 * Removes option of the given parameter
			 * @param {number} paramIndex index of the targeted parameter
			 * @param {string} optionIndex index of the targeted option
			 */
			deleteParamOption: function(paramIndex, optionIndex) {
				this.postprocessor.parameters[paramIndex].options.splice(optionIndex, 1);
			},
			/**
			 * Adds empty option to the given parameter
			 * @param {number} paramIndex index of the targeted parameter
			 */
			addParamOption: function(paramIndex) {
				this.postprocessor.parameters[paramIndex].options.push('');
			},
			/**
			 * Adds empty parameter
			 */
			addParam: function() {
				this.postprocessor.parameters.push({ param: '', options: ['']});
			},
			/**
			 * Deletes parameter
			 * @param {number} paramIndex index of the targeted parameter
			 */
			deleteParam: function(paramIndex) {
				this.postprocessor.parameters.splice(paramIndex, 1);
			},
			/**
			 * Close postprocess modal window
			 * @event close
			 */
			close: function() {
				this.$emit('close');
			},
			/**
			 * Fire action which postprocesses the given profile
			 */
			postprocessProfile: function() {
				this.$store.dispatch({
					type: 'postprocessProfile',
					path: this.originalRepositoryPath,
					registration: this.registered,
					profilePath: this.realpath,
					specification: this.postprocessor,
				});
				this.close();
			},
		},
	};
</script>

<style scoped>
	.postprocess .custom-modal {
		height: 560px;
	}
</style>