<template>
	<div>
		
		<removeModal v-show="isRemoveModalVisible" @close="closeModal" @confirm="unregisterProfile()">
			<span slot="header">Do you really wish to remove the performance profile <br><b>{{ rowToRemove.name }}</b>?</span>
		</removeModal>

		<div class="header-container" :class="isActive ? '' : 'bottom-border'">
			<div class="current-heading" @click="isActive = !isActive">
				<span>{{ this.heading }}</span>
				<span class="arrow" :class="isActive ? 'show' : 'hide' "></span>
			</div>
		</div>

		<div class="search-bar-container" v-if="isActive">
			<input type="text" class="search-bar" v-model="filterKey" placeholder="Search performance profiles">
		</div>

		<div class="main-table commit table-div table-striped table--striped table--md" v-if="isActive">
			
			<div class="table-header">
				
				<div class="row">
					<div class="col-lg-6">
						<div class="row">
							<div class="table-head align-left" v-for="(key, index) in tableColsFirst" :key="'tab1' + index" :class="getColSize(key, 'tableColsFirst')">
								<span class="text-uppercase" v-if="key != 'action'" @click="sortBy(key); sortArrow = !sortArrow">{{ key }}</span>
								<span class="arrow" v-if="key != 'action'" :class="sortArrow ? 'asc' : 'dsc'" @click="sortBy(key); sortArrow = !sortArrow"></span>
							</div>
						</div>
					</div>
					<div class="col-lg-6">
						<div class="row">
							<div class="table-head align-left" v-for="(key, index) in tableColsSecond" :key="'tab2' + index" :class="getColSize(key, 'tableColsSecond')">
								<span class="text-uppercase" v-if="key != 'action'" @click="sortBy(key); sortArrow = !sortArrow">{{ key }}</span>
								<span class="arrow" v-if="key != 'action'" :class="sortArrow ? 'asc' : 'dsc'" @click="sortBy(key); sortArrow = !sortArrow"></span>
							</div>
						</div>
					</div>
				</div>

			</div>

			<div class="table-body text-center">
				
				<span class="no-results" v-if="!profilesFiltered.length">No such performance profiles available</span>

				<div class="row table-row" v-for="(row,index) in profilesFiltered" :key="'mainrow' + index">
					
					<div class="col-lg-6">
						<div class="row">
							<template v-for="(value,col) in row">
								<div class="align-left" v-if="isTableColsFirst(col)" 
									:key="'row1' + col" :class="[getColSize(col, 'tableColsFirst'), col == 'status' ? 'degradation' : '', col == 'status' ? 'table-icon' : '']" 
									@click="goTo(row.id, row.commit)">
									
									<template v-if="col == 'type'">
										<div :class="value" class="profile-type-box">
											<span>{{ value }}</span>
										</div>
									</template>
									
									<template v-else>
										<template v-if="col == 'status'">
											<svg v-if="value == 'optimal'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M8 256C8 119 119 8 256 8s248 111 248 248-111 248-248 248S8 393 8 256zm292 116V256h70.9c10.7 0 16.1-13 8.5-20.5L264.5 121.2c-4.7-4.7-12.2-4.7-16.9 0l-115 114.3c-7.6 7.6-2.2 20.5 8.5 20.5H212v116c0 6.6 5.4 12 12 12h64c6.6 0 12-5.4 12-12z" fill="#009688"/></svg>
							
											<svg v-if="value == 'degrading'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M504 256c0 137-111 248-248 248S8 393 8 256 119 8 256 8s248 111 248 248zM212 140v116h-70.9c-10.7 0-16.1 13-8.5 20.5l114.9 114.3c4.7 4.7 12.2 4.7 16.9 0l114.9-114.3c7.6-7.6 2.2-20.5-8.5-20.5H300V140c0-6.6-5.4-12-12-12h-64c-6.6 0-12 5.4-12 12z" fill="#EF5350"/></svg>
										</template>
										<span>{{ value }}</span>
									</template>

								</div>
							</template>
						</div>
					</div>

					<div class="col-lg-6">
						<div class="row">
							<template v-for="(value,col) in row">
								<div class="align-left" v-if="isTableColsSecond(col)" 
									:key="'row2' + col"
									:class="[getColSize(col, 'tableColsSecond'), col == 'status' ? 'degradation' : '', col == 'status' ? 'table-icon' : '']" 
									@click.self="goTo(row.id, row.commit)">
							
									<template v-if="col == 'status'">
										<svg v-if="value == 'optimal'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M8 256C8 119 119 8 256 8s248 111 248 248-111 248-248 248S8 393 8 256zm292 116V256h70.9c10.7 0 16.1-13 8.5-20.5L264.5 121.2c-4.7-4.7-12.2-4.7-16.9 0l-115 114.3c-7.6 7.6-2.2 20.5 8.5 20.5H212v116c0 6.6 5.4 12 12 12h64c6.6 0 12-5.4 12-12z" fill="#009688"/></svg>
						
										<svg v-if="value == 'degrading'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M504 256c0 137-111 248-248 248S8 393 8 256 119 8 256 8s248 111 248 248zM212 140v116h-70.9c-10.7 0-16.1 13-8.5 20.5l114.9 114.3c4.7 4.7 12.2 4.7 16.9 0l114.9-114.3c7.6-7.6 2.2-20.5-8.5-20.5H300V140c0-6.6-5.4-12-12-12h-64c-6.6 0-12 5.4-12 12z" fill="#EF5350"/></svg>
									</template>

									<template v-if="col == 'action'">
										<div class="table-button remove" :name="row.id" v-if="type == 'registered'" @click="showModal(row.commit, row.id)">
											<span>remove</span>
											<!-- unregisterProfile(row.commit,row.id,row.path) -->
											<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
										</div>
										<div v-else class="table-button" :name="row.id" @click="registerProfile(row.commit,row.id,row.path)">
											<span>register</span>
											<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z" fill="white"/></svg>
										</div>
									</template>
									
									<template v-else-if="col == 'type'">
										<div :class="value" class="profile-type-box">
											<span>{{ value }}</span>
										</div>
									</template>
									
									<span v-else >{{ value }}</span>

								</div>

							</template>
						</div>
					</div>
				</div>
			</div>
			<div class="table-pagination" v-if="profilesFiltered.length">
				<div class="page-range">
					<span>Display per page: </span>
					<div class="range-number">
						<span :class="userItemsPerPage == 5 ? 'focus' : ''" @click="userItemsPerPage = itemsPerPage = 5; currentPage = 1">5</span>
						<span :class="userItemsPerPage == 10 ? 'focus' : ''" @click="userItemsPerPage = itemsPerPage = 10; currentPage = 1">10</span>
						<span :class="userItemsPerPage == 20 ? 'focus' : ''" @click="userItemsPerPage = itemsPerPage = 20; currentPage = 1">20</span>
						<span :class="userItemsPerPage == 50 ? 'focus' : ''" @click="userItemsPerPage = itemsPerPage = 50; currentPage = 1">50</span>
					</div>
				</div>
				<div class="page-numbering">
					<div v-if="currentPage > 1" @click="currentPage--" v-model="profilesFiltered"><span class="arrow hollow left"></span><span>PREVIOUS</span></div>
					<div class="page-number-container">
						<span class="page-number no-pointer">{{ currentPage }}</span>
						<span class="no-pointer"> of </span>
						<span class="page-number" @click="currentPage = numberPages" v-model="profilesFiltered">{{ numberPages }}</span>
					</div>
					<div v-if="currentPage < numberPages" @click="currentPage++" v-model="profilesFiltered"><span>NEXT</span><span class="arrow hollow right"></span></div>
				</div>
			</div>
		</div>
	</div>
</template>

<script type="text/javascript">
	export default {
		props: {
			tableRows: {
				type: Array,
				required: true,
				default: () => ({}),
			},
			tableColsFirst: {
				type: Array,
				required: true,
				default: () => ({}),
			},
			tableColsSecond: {
				type: Array,
				required: true,
				default: () => ({}),
			},
			type: {
				type: String,
				required: true,
				default: () => (""),
			},
			originCommit: {
				type: String,
				required: false,
			},
			heading: {
				type: String,
				required: true,
				default: () => (""),
			}
		},
		data: function() {
			return {
				sortOrder: ['asc'],
				sortKey: ['time'],
				sortArrow: false,
				filterKey: '',
				currentPage: 1,
				numberPages: '',
				itemsPerPage: 5,
				userItemsPerPage: 5,
				isActive: true,
				isRemoveModalVisible: false,
				rowToRemove: { commit: '', name: '' },
				originRepositoryPath: '',
			}
		},
		created: function() {
			this.originRepositoryPath = this.$store.getters.currentRepoPath;
		},
		computed: {
			/**
			 * Filteres displayed profiles based on the sorting key
			 */
			profilesFiltered: function () {
				
				var data = this.tableRows.filter((item) => {
					var keys = Object.keys(item);
					for (var i = 1; i < keys.length; i++) {
						if (item[keys[i]].match(this.filterKey)) {
							return true;
						}
					}
					return false;
				});

				this.numberPages = Math.ceil(data.length/this.itemsPerPage);
				data = data.slice(this.itemsPerPage * (this.currentPage - 1), this.itemsPerPage * this.currentPage);

				return _.orderBy(data, this.sortKey, this.sortOrder);
			}

		},
		methods: {
			/**
			 * Determines color of the profile boxes
			 * @param {string} value type of the profile, eg. memory, mixed or time
			 */
			determineColor: function(value) {
				if (value == 'mixed') {
					return '#673AB7';
				}
				else if (value == 'memory') {
					return '#3F51B5';
				}
				else {
					return '#03A9F4';
				}
			},
			/**
			 * Shows remove modal window
			 * @param {string} commit SHA of the targeted commit 
			 * @param {string} name ID of the targeted profile 
			 */
			showModal: function(commit, name) {
	    		this.isRemoveModalVisible = true;
	    		this.rowToRemove.commit = commit;
	    		this.rowToRemove.name = name;
	    	},
	    	/**
			 * Closes remove modal window
			 */
	    	closeModal: function() {
	    		this.isRemoveModalVisible = false;
	    		this.rowToRemove = { commit: '', name: '' };
	    	},
	    	/**
			 * Sets sorting parameters
			 */
			sortBy: function(key) {
				if (key == this.sortKey) {
					this.sortOrder = (this.sortOrder == 'asc') ? 'desc' : 'asc';
				} 
				else {
					this.sortOrder = 'asc';
					this.sortKey = key;
				}
			},
			/**
			 * Switches context
			 * @param {string} profileId id of the targeted profile
			 * @param {string} commitId id of the targeted commit
			 */
			goTo: function(profileId, commitId) {
				if (this.originCommit == undefined) {
					this.$router.push({ 
					name: 'profile',
					params: { 
						repo: this.$route.params.repo, 
						commit: commitId,
						profileId: profileId,
						originRepositoryPath: this.originRepositoryPath,
					}});
				}
				else {
					this.$router.push({ 
					name: 'profile',
					params: { 
						repo: this.$route.params.repo, 
						commit: this.originCommit,
						profileId: profileId,
						originRepositoryPath: this.originRepositoryPath,
					}});
				}
			},
			/**
			 * Determines column size depending on toggle panel options
			 * @param {string} item column to be targeted
			 * @param {string} toggle toggle identification
			 */
			getColSize: function(item, toggle) {
				if (toggle == 'tableColsFirst') {
					return 'col-lg-' + 12/this.tableColsFirst.length;
				}
				else {
					if (item == 'action') {
						return 'col-lg-3';
					}

					return 'col-lg-' + 12/this.tableColsSecond.length;
				}
			},
			/**
			 * Determines whether the given item belongs to the first toggle part
			 * @param {string} item column to be targeted
			 */
			isTableColsFirst: function(item) {
				return this.tableColsFirst.includes(item);
			},
			/**
			 * Determines whether the given item belongs to the second toggle part
			 * @param {string} item column to be targeted
			 */
			isTableColsSecond: function(item) {
				return this.tableColsSecond.includes(item);
			},
			/**
			 * Fires the action to register a performance profile
			 * @param {string} commitId SHA of the targeted commit
			 * @param {string} profileId id of the targeted profile
			 * @param {string} profilePath realpath to the targeted profile
			 */
			registerProfile: function(commitId, profileId, profilePath) {
				if (commitId == undefined) {
					commitId = this.$route.params.commit;
				}
				this.$store.dispatch({
					type: 'registerProfile',
					profileId: profileId,
					profilePath: profilePath,
					commitId: commitId,
					path: this.originRepositoryPath,
				})
			},
			/**
			 * Fires the action to unregister a performance profile
			 */
			unregisterProfile: function() {
				if (this.rowToRemove.commit == undefined) {
					this.rowToRemove.commit = this.$route.params.commit;
				}
				this.$store.dispatch({
					type: 'unregisterProfile',
					profileId: this.rowToRemove.name,
					commitId: this.rowToRemove.commit,
					path: this.originRepositoryPath,
				})
				this.closeModal();
			},
		},
	}
</script>