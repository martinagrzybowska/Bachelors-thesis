<template>
	<div>
		<div class="settings-item" v-for="item in settings">
			
			<span class="settings-item-heading">{{ item.name | capitalizeFirst }}</span>
			<span class="settings-item-subheading">{{ explanatoryNotes[item.name] }}</span>
							
			<template v-if="item.type == 'edit'">
				
				<div class="settings-item-input-container">
					<input type="text" class="search-bar" v-model="item.value">
					<div class="table-button" @click="saveChanges(type, item.name, 'value', item.value)">
						<span>save changes</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M433.941 129.941l-83.882-83.882A48 48 0 0 0 316.118 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V163.882a48 48 0 0 0-14.059-33.941zM224 416c-35.346 0-64-28.654-64-64 0-35.346 28.654-64 64-64s64 28.654 64 64c0 35.346-28.654 64-64 64zm96-304.52V212c0 6.627-5.373 12-12 12H76c-6.627 0-12-5.373-12-12V108c0-6.627 5.373-12 12-12h228.52c3.183 0 6.235 1.264 8.485 3.515l3.48 3.48A11.996 11.996 0 0 1 320 111.48z"/></svg>
					</div>
				</div>

				<template v-if="mode != 'global' && !item.value && !item.nearest">
					<span class="settings-item-heading secondary">Nearest set</span>
					<span class="settings-item-subheading secondary nearest">{{ item.nearest }}</span>
					<!-- <span class="settings-item-subheading secondary">{{ item.path }}</span> -->
					<!-- <div class="settings-item-input-container">
						<input type="text" class="search-bar" v-model="item.nearest">
						<div class="table-button" @click="saveChanges(type, item.name, 'nearest', item.nearest)">
							<span>save changes</span>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M433.941 129.941l-83.882-83.882A48 48 0 0 0 316.118 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V163.882a48 48 0 0 0-14.059-33.941zM224 416c-35.346 0-64-28.654-64-64 0-35.346 28.654-64 64-64s64 28.654 64 64c0 35.346-28.654 64-64 64zm96-304.52V212c0 6.627-5.373 12-12 12H76c-6.627 0-12-5.373-12-12V108c0-6.627 5.373-12 12-12h228.52c3.183 0 6.235 1.264 8.485 3.515l3.48 3.48A11.996 11.996 0 0 1 320 111.48z"/></svg>
						</div>
					</div> -->
				</template>

			</template>
						
			<template v-else-if="item.type == 'radio'">
				
				<div class="settings-item-radio-container">
					<div>
						<div v-for="option in pagingOptions" :key="option">
							<input type="radio" name="radio" :value="option" v-model="item.value">
							<span>{{ option }}</span>
						</div>
					</div>
					<div class="table-button" @click="saveChanges(type, item.name, 'value', item.value)">
						<span>save changes</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M433.941 129.941l-83.882-83.882A48 48 0 0 0 316.118 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V163.882a48 48 0 0 0-14.059-33.941zM224 416c-35.346 0-64-28.654-64-64 0-35.346 28.654-64 64-64s64 28.654 64 64c0 35.346-28.654 64-64 64zm96-304.52V212c0 6.627-5.373 12-12 12H76c-6.627 0-12-5.373-12-12V108c0-6.627 5.373-12 12-12h228.52c3.183 0 6.235 1.264 8.485 3.515l3.48 3.48A11.996 11.996 0 0 1 320 111.48z"/></svg>
					</div>
				</div>
				
				<template v-if="mode != 'global' && !item.value && !item.nearest">
					
					<span class="settings-item-heading secondary">Nearest set</span>
					<span class="settings-item-subheading secondary">{{ item.path }}</span>
					
					<div class="settings-item-radio-container">
						<div>
							<div v-for="option in pagingOptions" :key="option">
								<input type="radio" name="radio" :value="option" v-model="item.nearest">
								<span>{{ option }}</span>
							</div>
						</div>
						<!-- <div class="table-button" @click="saveChanges(type, item.name, 'nearest', item.nearest)">
							<span>save changes</span>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M433.941 129.941l-83.882-83.882A48 48 0 0 0 316.118 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V163.882a48 48 0 0 0-14.059-33.941zM224 416c-35.346 0-64-28.654-64-64 0-35.346 28.654-64 64-64s64 28.654 64 64c0 35.346-28.654 64-64 64zm96-304.52V212c0 6.627-5.373 12-12 12H76c-6.627 0-12-5.373-12-12V108c0-6.627 5.373-12 12-12h228.52c3.183 0 6.235 1.264 8.485 3.515l3.48 3.48A11.996 11.996 0 0 1 320 111.48z"/></svg>
						</div> -->
					</div>
				</template>	

			</template>

			<template v-else-if="item.type == 'checkbox'">

				<template v-for="(value, action) in item.actions">
					
					<span class="settings-item-heading secondary" :key="'row11' + value" >{{ action | capitalizeFirst }}</span>
					
					<div class="settings-item-radio-container" :key="'row12' + value">
						<div>
							<template v-for="option in value">
								<div v-for="(checked, key) in option" :key="'row3' + key">
									<input type="checkbox" value="key" v-model="option[key]">
									<span>{{ key }}</span>
								</div>
							</template>
						</div>
						<div class="table-button" @click="saveChanges(type, item.name, 'actions.' + action, value)">
							<span>save changes</span>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M433.941 129.941l-83.882-83.882A48 48 0 0 0 316.118 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V163.882a48 48 0 0 0-14.059-33.941zM224 416c-35.346 0-64-28.654-64-64 0-35.346 28.654-64 64-64s64 28.654 64 64c0 35.346-28.654 64-64 64zm96-304.52V212c0 6.627-5.373 12-12 12H76c-6.627 0-12-5.373-12-12V108c0-6.627 5.373-12 12-12h228.52c3.183 0 6.235 1.264 8.485 3.515l3.48 3.48A11.996 11.996 0 0 1 320 111.48z"/></svg>
						</div>
					</div>

				</template>

			</template>

			<template v-else-if="item.type == 'blank'">
				<span class="settings-item-subheading">Version Control System type is <b>{{ item.value | capitalizeFirst }}</b> located at {{ item.path }}</span>
			</template>

		</div>
	</div>
</template>

<script type="text/javascript">
	export default {
		props: {
			pagingOptions: {
				type: Array,
				required: false,
				default: () => ([]),
			},
			settings: {
				type: Array,
				required: true,
				default: () => ([]),
			},
			type: {
				type: String,
				required: true,
				default: () => (""),
			},
			type: {
				type: String,
				required: false,
				default: () => (""),
			},
		},
		data: function() {
			return {
				explanatoryNotes: {
					status: 'Specifies the formatting string for the output of the perun status command',
					log: 'Specifies the formatting string for the output of the short format of perun log command',
					"output profile template": 'Specifies the format for automatic generation of profile files',
					paging: 'Sets the paging for perun log and perun status',
					editor: 'Sets user choice of text editor used for manual text-editing of configuration files of Perun',
					"perun hooks": 'Custom scripts designed to fire off when certain important actions occur',
				},
			}
		},
		methods: {
			/**
			 * Fires action which saves settings
			 * @param {string} settingSection section which is to be targeted, eg. general, format ...
			 * @param {string} settingName subsection which is to be targeted, eg. status, log ...
			 * @param {string} settingItem which item was saved, either value or nearest
			 * @param {string} settingValue new value
			 */
			saveChanges: function(settingSection, settingName, settingItem, settingValue) {
				if (this.$route.params.repo == undefined) {
					this.$store.dispatch({
						type: 'saveGlobalSettings',
						section: settingSection,
						name: settingName,
						value: settingValue,
					});
				}
				else {
					this.$store.dispatch({
						type: 'saveLocalSettings',
						path: this.originRepositoryPath,
						section: settingSection,
						name: settingName,
						item: settingItem,
						value: settingValue,
					});
				}
			},
		},
		computed: {
			/**
			 * Gets current repository path from shared state
			 */
			originRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			},
		},
	}
</script>

