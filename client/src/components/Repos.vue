<template>
	<div class="main-container">
		
		<transition name="fade">
			<removeModal v-show="isRemoveModalVisible" @close="closeModal()" @confirm="removeRepo()">
					<span slot="header">Do you really wish to remove the Perun wrapper over the repository <b>{{ rowToRemove.name | capitalizeFirst }}</b>?</span>
			</removeModal>
		</transition>

		<div class="container">

			<div class="header-search-container">

				<div class="search-bar-container">
					<input type="text" class="search-bar repos" v-model="pathToSearch" placeholder="Start searching at path eg. /Users/Home/Desktop" @keyup.enter="loadRepositories()">
				</div>
				<div class="table-button search" @click="loadRepositories()">

					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"/></svg>
				</div>

			</div>

			<div class="header-container">
				<div class="current-heading">
					<p>Overview of encountered repositories</p>
				</div>
			</div>
			
			<div class="content-container">
				
				<div class="search-bar-container">
					 <input type="text" class="search-bar" v-model="filterKey" placeholder="Search displayed repositories">
				</div>
				
				<div class="main-table repositories table-div table-striped table--striped table--md">
					
					<div class="table-header">
						<div class="row">
							<div class="table-head align-left" v-for="(value, key) in tableCols" :key="key" :class="key == 'path' ? 'col-lg-3' : 'col-lg-2'">
								<span class="text-uppercase" @click="sortBy(key); sortArrow = !sortArrow">{{ value }}</span>
								<span class="arrow" v-if="value != ''" :class="sortArrow ? 'asc' : 'dsc'" @click="sortBy(key); sortArrow = !sortArrow"></span>
							</div>
						</div>
					</div>
					
					<div class="table-body text-center">
						
						<span class="no-results" v-if="!reposFiltered.length">No such repositories available</span>
						
						<div class="row table-row" v-for="row in reposFiltered" :key="row.path">
							
							<div class="col-lg-2 align-left" @click="goTo(row)">
								<span>{{ row.name | capitalizeFirst }}</span>
							</div>
							
							<div class="col-lg-3 align-left" @click="goTo(row)">
								<span>{{ row.path }}</span>
							</div>
							
							<div class="col-lg-2 align-left" @click="goTo(row)">
								<span>{{ row.vcs_type | capitalizeFirst }}</span>
							</div>
							
							<template v-if="row.integration == 'integrated'">
								
								<div class="col-lg-2 align-left perun-integration table-icon" key="already-integrated-sign" @click="goTo(row)">
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M504 256c0 136.967-111.033 248-248 248S8 392.967 8 256 119.033 8 256 8s248 111.033 248 248zM227.314 387.314l184-184c6.248-6.248 6.248-16.379 0-22.627l-22.627-22.627c-6.248-6.249-16.379-6.249-22.628 0L216 308.118l-70.059-70.059c-6.248-6.248-16.379-6.248-22.628 0l-22.627 22.627c-6.248 6.248-6.248 16.379 0 22.627l104 104c6.249 6.249 16.379 6.249 22.628.001z" class="st1" fill="#00897b"/></svg>
									<span>integrated</span>
								</div>
								
								<div class="col-lg-2 align-left perun-action" key="already-integrated-button">
									
									<div class="table-button remove" @click="showModal(row)">
										<div>
											<span>remove</span>
										</div>
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
									</div>

								</div>

							</template>
							
							<template v-else-if="row.integration == 'missing'">
								
								<div class="col-lg-2 align-left perun-integration table-icon" key="missing-integration-sign">
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm121.6 313.1c4.7 4.7 4.7 12.3 0 17L338 377.6c-4.7 4.7-12.3 4.7-17 0L256 312l-65.1 65.6c-4.7 4.7-12.3 4.7-17 0L134.4 338c-4.7-4.7-4.7-12.3 0-17l65.6-65-65.6-65.1c-4.7-4.7-4.7-12.3 0-17l39.6-39.6c4.7-4.7 12.3-4.7 17 0l65 65.7 65.1-65.6c4.7-4.7 12.3-4.7 17 0l39.6 39.6c4.7 4.7 4.7 12.3 0 17L312 256l65.6 65.1z" fill="#ff574b"/></svg>
									<span>missing</span>
								</div>
								
								<div class="col-lg-2 align-left perun-action" key="missing-integration-button">
									<div class="table-button" @click="integrateRepo(row)">
										<div>
											<span>integrate</span>
										</div>
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z"/></svg>
									</div>
								</div>

							</template>

						</div>
					</div>

					<div class="table-pagination" v-if="reposFiltered.length">
						
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
							<div v-if="currentPage > 1" @click="currentPage--" v-model="reposFiltered"><span class="arrow hollow left"></span><span>PREVIOUS</span></div>
							<div class="page-number-container">
								<span class="page-number no-pointer">{{ currentPage }}</span>
								<span class="no-pointer"> of </span>
								<span class="page-number" @click="currentPage = numberPages" v-model="reposFiltered">{{ numberPages }}</span>
							</div>
							<div v-if="currentPage < numberPages" @click="currentPage++" v-model="reposFiltered"><span>NEXT</span><span class="arrow hollow right"></span></div>
						</div>

					</div>

				</div>
			</div>
		</div>
	</div>
</template>

<script type="text/javascript">
	export default {
		data: function () {
			return {
				tableCols: {
					name: 'Repository name',
					path: 'Path to repository',
					vcs_type: 'VCS type',
					integration: 'Perun integration',
					action: ''
				},
				displayNumber: '',
				sortOrder: ['asc'],
				sortKey: ['name'],
				sortArrow: false,
				filterKey: '',
				currentPage: 1,
				numberPages: '',
				pathToSearch: '',
				itemsPerPage: 5,
				userItemsPerPage: 5,
				isSuccessModalVisible: false,
				isRemoveModalVisible: false,
				isErrorModalVisible: false,
				rowToRemove: { name: '', path: '' },
			}
		},
		created: function() {
			this.pathToSearch = this.$store.getters.searchPath;
		},
		computed: {
			/**
			 * Gets repositories list from the shared state
			 */
			tableRows: function() {	
				return this.$store.getters.repositories;
			},
			/**
			 * Filters displayed repositories based on the sorting key
			 */
			reposFiltered: function () {
				var data = this.tableRows.filter((repo) => {
					var keys = Object.keys(repo);
					for (var i = 0; i < keys.length; i++) {
						if (repo[keys[i]].match(this.filterKey)) {
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
			 * Shows remove modal window
			 * @param {Object} row to remove
			 */
			showModal: function(row) {
    			this.isRemoveModalVisible = true;
    			this.rowToRemove = row;
	    	},
	    	/**
			 * Close remove modal window
			 */
	    	closeModal: function() {
    			this.isRemoveModalVisible = false;
    			setTimeout(() => {
    				this.rowToRemove = { name: '', path: '' };
    			}, 220);
	    	},
	    	/**
			 * Set sorting settings
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
			 * Fire action that loads repositories based on the path
			 */
			loadRepositories: function() {
				this.$store.dispatch({
					type: 'changeSearchPath',
					path: this.pathToSearch,
				});
				this.$store.dispatch({
					type: 'loadRepositories',
					path: this.pathToSearch,
				});
			},
			/**
			 * Fire action that creates Perun instance
			 * @param {Object} repo to create the wrapper over  
			 */
			integrateRepo: function(repo) {
				this.$store.dispatch({
					type: 'integrateRepo',
					path: repo.path,
				});
			},
			/**
			 * Fire action that removes Perun instance
			 */
			removeRepo: function() {	
				this.$store.dispatch({
					type: 'removeRepoIntegration',
					path: this.rowToRemove.path,
				})
				this.closeModal();
			},
			/**
			 * Change context to repository dashboard
			 * @param {Object} repository to set the context to
			 */
			goTo: function(repository) {		
				if (repository.integration == 'integrated') {
					this.$store.dispatch('setCurrentRepoName', repository.name);
					this.$store.dispatch('setCurrentRepoPath', repository.path);

					this.$router.push({ 
						name: 'dashboard',
						params: { repo: repository.name, integration:repository.integration, originRepositoryPath: repository.path,
					}});
				}
			},
		},
	}
</script>