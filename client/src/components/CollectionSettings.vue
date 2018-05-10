<template>
	<div>
		<div class="settings-item job-matrix">
			
			<div>
				<span class="settings-item-heading">Specification of profiled commands</span>
				<span class="settings-item-subheading">Collection specification</span>
			</div>

			<div class="commands-item" v-for="(value, key, index) in localProfiledCommands" :key="'commands' + index">
				
				<div>
					<span class="settings-item-heading secondary">{{ key | capitalizeFirst}}</span>
					<div class="settings-item-input-container profiled-commands" v-for="(item, index) in value" :key="'profiles' + index">
						<input type="text" class="search-bar" v-model="value[index]">
						<div class="settings-item-input-add" @click="deleteItem(key,index)">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M0 84V56c0-13.3 10.7-24 24-24h112l9.4-18.7c4-8.2 12.3-13.3 21.4-13.3h114.3c9.1 0 17.4 5.1 21.5 13.3L312 32h112c13.3 0 24 10.7 24 24v28c0 6.6-5.4 12-12 12H12C5.4 96 0 90.6 0 84zm416 56v324c0 26.5-21.5 48-48 48H80c-26.5 0-48-21.5-48-48V140c0-6.6 5.4-12 12-12h360c6.6 0 12 5.4 12 12zm-272 68c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208z"/></svg>
						</div>
					</div>
				</div>
				
				<div class="settings-item-input-add collection-specification">
					<svg @click="addEmpty(key)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M448 294.2v-76.4c0-13.3-10.7-24-24-24H286.2V56c0-13.3-10.7-24-24-24h-76.4c-13.3 0-24 10.7-24 24v137.8H24c-13.3 0-24 10.7-24 24v76.4c0 13.3 10.7 24 24 24h137.8V456c0 13.3 10.7 24 24 24h76.4c13.3 0 24-10.7 24-24V318.2H424c13.3 0 24-10.7 24-24z"/></svg>
				</div>
				
				<div class="settings-item-buttons">
					<div v-if="mode == 'job-matrix'" class="table-button" @click="saveChanges('profiledCommands', key, value)">
						<span>save changes</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M433.941 129.941l-83.882-83.882A48 48 0 0 0 316.118 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V163.882a48 48 0 0 0-14.059-33.941zM224 416c-35.346 0-64-28.654-64-64 0-35.346 28.654-64 64-64s64 28.654 64 64c0 35.346-28.654 64-64 64zm96-304.52V212c0 6.627-5.373 12-12 12H76c-6.627 0-12-5.373-12-12V108c0-6.627 5.373-12 12-12h228.52c3.183 0 6.235 1.264 8.485 3.515l3.48 3.48A11.996 11.996 0 0 1 320 111.48z"/></svg>
					</div>
					<div v-if="mode == 'job-matrix'" class="table-button reload" @click="revertChanges('profiledCommands', key)">
						<span>undo all changes</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M255.545 8c-66.269.119-126.438 26.233-170.86 68.685L48.971 40.971C33.851 25.851 8 36.559 8 57.941V192c0 13.255 10.745 24 24 24h134.059c21.382 0 32.09-25.851 16.971-40.971l-41.75-41.75c30.864-28.899 70.801-44.907 113.23-45.273 92.398-.798 170.283 73.977 169.484 169.442C423.236 348.009 349.816 424 256 424c-41.127 0-79.997-14.678-110.63-41.556-4.743-4.161-11.906-3.908-16.368.553L89.34 422.659c-4.872 4.872-4.631 12.815.482 17.433C133.798 479.813 192.074 504 256 504c136.966 0 247.999-111.033 248-247.998C504.001 119.193 392.354 7.755 255.545 8z"/></svg>
					</div>
				</div>
			</div>
		</div>

		<div class="settings-item job-matrix">
			
			<div>
				<span class="settings-item-heading">Collection specification</span>
				<span class="settings-item-subheading">Collection specification</span>
			</div>

			<div class="collection-specification-container commands-item" v-for="(contents, type) in localCollectionSpecification" :key="type">
				<div>
					<span class="settings-item-heading secondary">{{ type | capitalizeFirst }}</span>
					
					<div class="settings-item collection-specification" v-for="(item, itemIndex) in contents" :key="'item' + itemIndex">

						<span class="settings-item-heading secondary">Name</span>
						<div class="settings-item-input-container collection-specification">
							<input type="text" class="search-bar" v-model="item.name" >
						</div>

						<div class="collection-specification-params">
							<div class="parameters">
								<span class="settings-item-heading secondary">Parameters</span>
							</div>
							<div class="values">
								<span class="settings-item-heading secondary">Values</span>
							</div>
						</div>
						
						<div v-if="item.parameters.length == 0" class="settings-item-input-add" @click="addParam(type,itemIndex)">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M448 294.2v-76.4c0-13.3-10.7-24-24-24H286.2V56c0-13.3-10.7-24-24-24h-76.4c-13.3 0-24 10.7-24 24v137.8H24c-13.3 0-24 10.7-24 24v76.4c0 13.3 10.7 24 24 24h137.8V456c0 13.3 10.7 24 24 24h76.4c13.3 0 24-10.7 24-24V318.2H424c13.3 0 24-10.7 24-24z"/></svg>
						</div>
						
						<div class="collection-specification-params" v-for="(param, paramIndex) in item.parameters" :key="'parameter' + paramIndex">
							
							<div class="parameters">
								<div>
									<input type="text" class="search-bar" v-model="param.param" >
									<div class="settings-item-input-add" @click="deleteParam(type,itemIndex,paramIndex)">
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M0 84V56c0-13.3 10.7-24 24-24h112l9.4-18.7c4-8.2 12.3-13.3 21.4-13.3h114.3c9.1 0 17.4 5.1 21.5 13.3L312 32h112c13.3 0 24 10.7 24 24v28c0 6.6-5.4 12-12 12H12C5.4 96 0 90.6 0 84zm416 56v324c0 26.5-21.5 48-48 48H80c-26.5 0-48-21.5-48-48V140c0-6.6 5.4-12 12-12h360c6.6 0 12 5.4 12 12zm-272 68c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208z"/></svg>
									</div>
									<span class="secondary">:</span>
								</div>
								<div v-if="(paramIndex + 1) == item.parameters.length" class="settings-item-input-add" @click="addParam(type,itemIndex)">
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M448 294.2v-76.4c0-13.3-10.7-24-24-24H286.2V56c0-13.3-10.7-24-24-24h-76.4c-13.3 0-24 10.7-24 24v137.8H24c-13.3 0-24 10.7-24 24v76.4c0 13.3 10.7 24 24 24h137.8V456c0 13.3 10.7 24 24 24h76.4c13.3 0 24-10.7 24-24V318.2H424c13.3 0 24-10.7 24-24z"/></svg>
								</div>
							</div>
							
							<div class="values">
								<div class="value-inputs-container">
									<template v-for="(option, optionIndex) in param.options">
										<input type="text" class="search-bar" v-model="param.options[optionIndex]" :key="'searchbar' + optionIndex">
										<div class="settings-item-input-add"  @click="deleteParamOption(type,itemIndex,paramIndex,optionIndex)" :key="'wrapper' + optionIndex">
											<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M0 84V56c0-13.3 10.7-24 24-24h112l9.4-18.7c4-8.2 12.3-13.3 21.4-13.3h114.3c9.1 0 17.4 5.1 21.5 13.3L312 32h112c13.3 0 24 10.7 24 24v28c0 6.6-5.4 12-12 12H12C5.4 96 0 90.6 0 84zm416 56v324c0 26.5-21.5 48-48 48H80c-26.5 0-48-21.5-48-48V140c0-6.6 5.4-12 12-12h360c6.6 0 12 5.4 12 12zm-272 68c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208z"/></svg>
										</div>
									</template>
									<div class="settings-item-input-add" @click="addParamOption(type,itemIndex,paramIndex)">
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M448 294.2v-76.4c0-13.3-10.7-24-24-24H286.2V56c0-13.3-10.7-24-24-24h-76.4c-13.3 0-24 10.7-24 24v137.8H24c-13.3 0-24 10.7-24 24v76.4c0 13.3 10.7 24 24 24h137.8V456c0 13.3 10.7 24 24 24h76.4c13.3 0 24-10.7 24-24V318.2H424c13.3 0 24-10.7 24-24z"/></svg>
									</div>
								</div>
							</div>

						</div>

						<div class="settings-item-input-container profiled-commands collection-specification">
							<div class="table-button remove" @click="deleteCategory(type, categoryIndex)">
								<span>delete</span>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M0 84V56c0-13.3 10.7-24 24-24h112l9.4-18.7c4-8.2 12.3-13.3 21.4-13.3h114.3c9.1 0 17.4 5.1 21.5 13.3L312 32h112c13.3 0 24 10.7 24 24v28c0 6.6-5.4 12-12 12H12C5.4 96 0 90.6 0 84zm416 56v324c0 26.5-21.5 48-48 48H80c-26.5 0-48-21.5-48-48V140c0-6.6 5.4-12 12-12h360c6.6 0 12 5.4 12 12zm-272 68c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208zm96 0c0-8.8-7.2-16-16-16s-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208z"/></svg>
							</div>
						</div>

					</div>
				</div>
				
				<div class="settings-item-input-add" @click="addCategory(type)">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M448 294.2v-76.4c0-13.3-10.7-24-24-24H286.2V56c0-13.3-10.7-24-24-24h-76.4c-13.3 0-24 10.7-24 24v137.8H24c-13.3 0-24 10.7-24 24v76.4c0 13.3 10.7 24 24 24h137.8V456c0 13.3 10.7 24 24 24h76.4c13.3 0 24-10.7 24-24V318.2H424c13.3 0 24-10.7 24-24z"/></svg>
				</div>
				
				<div class="settings-item-buttons">
					<div v-if="mode == 'job-matrix'" class="table-button" @click="saveChanges('collectionSpecification', type, contents)">
						<span>save changes</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M433.941 129.941l-83.882-83.882A48 48 0 0 0 316.118 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V163.882a48 48 0 0 0-14.059-33.941zM224 416c-35.346 0-64-28.654-64-64 0-35.346 28.654-64 64-64s64 28.654 64 64c0 35.346-28.654 64-64 64zm96-304.52V212c0 6.627-5.373 12-12 12H76c-6.627 0-12-5.373-12-12V108c0-6.627 5.373-12 12-12h228.52c3.183 0 6.235 1.264 8.485 3.515l3.48 3.48A11.996 11.996 0 0 1 320 111.48z"/></svg>
					</div>
					<div v-if="mode == 'job-matrix'" class="table-button reload" @click="revertChanges('collectionSpecification', type)">
						<span>undo all changes</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M255.545 8c-66.269.119-126.438 26.233-170.86 68.685L48.971 40.971C33.851 25.851 8 36.559 8 57.941V192c0 13.255 10.745 24 24 24h134.059c21.382 0 32.09-25.851 16.971-40.971l-41.75-41.75c30.864-28.899 70.801-44.907 113.23-45.273 92.398-.798 170.283 73.977 169.484 169.442C423.236 348.009 349.816 424 256 424c-41.127 0-79.997-14.678-110.63-41.556-4.743-4.161-11.906-3.908-16.368.553L89.34 422.659c-4.872 4.872-4.631 12.815.482 17.433C133.798 479.813 192.074 504 256 504c136.966 0 247.999-111.033 248-247.998C504.001 119.193 392.354 7.755 255.545 8z"/></svg>
					</div>
				</div>

			</div>
		</div>
	</div>
</template>

<script type="text/javascript">
	export default {
		props: {
			modalProfiledCommands: {
				type: Object,
				default: () => ({}),
			},
			modalCollectionSpecification: {
				type: Object,
				default: () => ({}),
			},
			mode: {
				type: String,
				required: false,
				default: () => (""),
			},
		},
		data: function() {
			return {
				localProfiledCommands: '',
				localCollectionSpecification: '',
				originRepositoryPath: '',
			}
		},
		created: function() {
			if (this.mode == 'job-matrix') {
				this.localProfiledCommands = this.$store.getters.localSettings.jobMatrix.profiledCommands;
				this.localCollectionSpecification = this.$store.getters.localSettings.jobMatrix.collectionSpecification;
			}
			else {
				this.localProfiledCommands = this.modalProfiledCommands;
				this.localCollectionSpecification = this.modalCollectionSpecification;
			}
			this.originRepositoryPath = this.$store.getters.currentRepoPath;
		},
		methods: {
			/**
			 * Adds empty input field to the given category of profiled commands, eg. args
			 * @param {string} category specifies the input's category
			 */
			addEmpty: function(category) {
				this.localProfiledCommands[category].push('');
			},
			/**
			 * Deletes input field at index of the given category of profiled commands, eg. args
			 * @param {string} category specifies the input's category
			 * @param {number} index of the input field
			 */
			deleteItem: function(category, index) {
				this.localProfiledCommands[category].splice(index, 1);
			},
			/**
			 * Deletes input field of an option parameter at the index of the given category 
			 * @param {string} category specifies the input's category
			 * @param {number} categoryIndex index within the category
			 * @param {number} paramIndex index of the param
			 * @param {number} optionIndex index of the option
			 */
			deleteParamOption: function(category, categoryIndex, paramIndex, optionIndex) {
				this.localCollectionSpecification[category][categoryIndex].parameters[paramIndex].options.splice(optionIndex, 1);
			},
			/**
			 * Adds input field of an option parameter to the given category 
			 * @param {string} category specifies the input's category
			 * @param {number} categoryIndex index within the category
			 * @param {number} paramIndex index of the param
			 */
			addParamOption: function(category, categoryIndex, paramIndex) {
				this.localCollectionSpecification[category][categoryIndex].parameters[paramIndex].options.push('');
			},
			/**
			 * Adds input field of a parameter to the given category 
			 * @param {string} category specifies the input's category
			 * @param {number} categoryIndex index within the category
			 */
			addParam: function(category, categoryIndex) {
				this.localCollectionSpecification[category][categoryIndex].parameters.push({ param: '', options: ['']});
			},
			/**
			 * Deletes input field of a parameter at the index of the given category 
			 * @param {string} category specifies the input's category
			 * @param {number} categoryIndex index within the category
			 * @param {number} paramIndex index of the param
			 */
			deleteParam: function(category, categoryIndex, paramIndex) {
				this.localCollectionSpecification[category][categoryIndex].parameters.splice(paramIndex, 1);
			},
			/**
			 * Adds empty input to the category of collection specification, eg. collectors
			 * @param {string} category specifies the input's category
			 */
			addCategory: function(category) {
				this.localCollectionSpecification[category].push({ name: '', parameters: [ { param: '', options: [''] } ] } );
			},
			/**
			 * Deletes input of the category of collection specification, eg. collectors
			 * @param {string} category specifies the input's category
			 * @param {number} categoryIndex index of the category input
			 */
			deleteCategory: function(category, categoryIndex) {
				this.localCollectionSpecification[category].splice(categoryIndex, 1);
			},
			/**
			 * Capitalizes the first letter
			 * @param {string} string to capitalize
			 */
			capFirst: function(string) {
				return string.charAt(0).toUpperCase() + string.slice(1);
			},
			/**
			 * Reverts all unsaved changes of a category
			 * @param {string} section to target
			 * @param {string} subsection to revert changes
			 */
			revertChanges: function(section, subsection) {
				var current_section = 'local' + this.capFirst(section);
				var copy = JSON.parse(JSON.stringify(this.$store.getters.revertLocalSettings.jobMatrix[section][subsection]));
				this.$set(this[current_section], subsection, copy);
			},
			/**
			 * Fires action for saving the changes
			 * @param {string} settingSection which section to target, eg. profiled commands or collection specification
			 * @param {string} settingName name of the subsections, eg. command, workload, or collectors ...
			 * @param {string, Object} settingValue new value which is to be set
			 */
			saveChanges: function(settingSection, settingName, settingValue) {
				if (settingValue != undefined) {
					settingValue = this.checkEmptyKeys(settingSection, settingName, settingValue);
					this.$store.dispatch({
						type: 'saveJobMatrixSettings',
						path: this.originRepositoryPath,
						section: settingSection,
						name: settingName,
						value: settingValue,
					});
				}
			},
			/**
			 * Deletes all empty keys before saving changes
			 * @param {string} settingSection which section to target, eg. profiled commands or collection specification
			 * @param {string} settingName name of the subsections, eg. command, workload, or collectors ...
			 * @param {string, Object} settingValue new value which is to be set
			 */
			checkEmptyKeys: function(settingSection, settingName, settingValue) {
				var output = JSON.parse(JSON.stringify(settingValue));
				if (settingSection == 'collectionSpecification') {
					for (var iter = 0; iter < settingValue.length; iter++) {
						if (settingValue[iter].name == '') {
							output.splice(iter, 1);
							continue;
						}
						
						for (var iter_param = 0; iter_param < settingValue[iter].parameters.length; iter_param++) {
							if (settingValue[iter].parameters[iter_param].param == '') {
								output[iter].parameters.splice(iter_param , 1);
								continue;
							}
							for (var iter_opt = 0; iter_opt < settingValue[iter].parameters[iter_param].options.length; iter_opt++) {
								if (settingValue[iter].parameters[iter_param].options[iter_opt] == '') {
									output[iter].parameters[iter_param].options.splice(iter_opt , 1);
									continue;
								}
							}
							if (output[iter].parameters[iter_param].options.length == 0) {
								delete output[iter].parameters[iter_param].options
							}
						}
						if (output[iter].parameters.length == 0) {
							delete output[iter].parameters;
						}
					}
				}
				else {
					for (var iter = 0; iter < settingValue.length; iter++) {
						if (settingValue[iter] == '') {
							output.splice(iter, 1);
						}
					}
				}
				return output;
			}
		}
	}
</script>