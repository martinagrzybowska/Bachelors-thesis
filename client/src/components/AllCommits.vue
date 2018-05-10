<template>
	<div class="main-container">

		<sidebar></sidebar>
		
		<div class="container">
			
			<div class="header-container">
				
				<div class="current-heading">
					<p>Minor versions list of</p>
					<select v-model="currentBranch" class="selectpicker">
						<option disabled value="">Please select one</option>
						<option v-for="branch in optionalBranches" :key="branch">{{ branch }}</option>
					</select>
				</div>
				
				<div class="current-heading right">
					<p>repository <span>{{ this.$route.params.repo | capitalizeFirst }}</span></p>
				</div>

			</div>
			
			<div class="content-container">
				
				<template v-if="!tableRows.length">
					<smilingCookie><span slot="item">commits</span></smilingCookie>
				</template>
				
				<template v-else>
					
					<div class="search-bar-container">
						 <input type="text" class="search-bar" v-model="filterKey" placeholder="Search minor versions">
					</div>

					<div class="main-table commits table-div table-striped table--striped table--md">
						
						<div class="table-header">
							<div class="row">
								<div class="table-head align-left" :class="key != 'performance_info' ? 'col-lg-2': 'col-lg-4'" v-for="(value, key) in tableCols" :key="value">
									<template v-if="key != 'performance'">
										<template v-if="(key != 'performance_info') && (key != 'profiles')">
											<span class="text-uppercase" @click="sortBy(key); sortArrow = !sortArrow">{{ value }}</span>
											<span class="arrow" v-if="value != ''" :class="sortArrow ? 'asc' : 'dsc'" @click="sortBy(key); sortArrow = !sortArrow"></span>
										</template>
										<template v-else>
											<span class="text-uppercase">{{ value }}</span>
										</template>
									</template>
								</div>
							</div>
						</div>

						<div class="table-body text-center">
							<span class="no-results" v-if="!commitsFiltered.length">No such minor versions available</span>

							<div class="row table-row" v-for="row in commitsFiltered" :key="row.id">
								<div class="col-lg-2 align-left" @click="goTo(row)">
									<div class="commit-head-box" v-if="row.head == 'head'">HEAD</div>
									<span>{{ row.minor_version }}</span>
								</div>
								<div class="col-lg-2 align-left" @click="goTo(row)">
									<span>"{{ row.message }}"</span>
								</div>
								<div class="col-lg-2 align-left" @click="goTo(row)">
									<span>{{ row.date }}</span>
								</div>
								<div class="col-lg-2 align-left" @click="goTo(row)">
									<div class="profile-numbers-box time" :class="determineStyle(row.profiles.time)" title="time">{{ row.profiles.time }}</div>
									<div class="profile-numbers-box memory" :class="determineStyle(row.profiles.memory)" title="memory">{{ row.profiles.memory }}</div>
									<div class="profile-numbers-box mixed" :class="determineStyle(row.profiles.mixed)" title="mixed">{{ row.profiles.mixed }}</div>
									<div>-</div>
									<div class="profile-numbers-box all" :class="determineStyle(row.profiles.all)" title="all">{{ row.profiles.all }}</div>
								</div>
								<div class="col-lg-4 align-left degradation-miniinfo table-icon" @click="goTo(row)">

									<div class="profile-numbers-box degradation" :class="determineStyle(row.performance_info.Degradation)" title="degradation">{{ row.performance_info.Degradation }}</div>

									<div class="profile-numbers-box maybe-degradation" :class="determineStyle(row.performance_info.MaybeDegradation)" title="maybe-degradation">{{ row.performance_info.MaybeDegradation }}</div>

									<div class="profile-numbers-box no-change" :class="determineStyle(row.performance_info.NoChange)" title="no-change">{{ row.performance_info.NoChange }}</div>

									<div class="profile-numbers-box maybe-optimalization" :class="determineStyle(row.performance_info.MaybeOptimization)" title="maybe-optimalization">{{ row.performance_info.MaybeOptimization }}</div>

									<div class="profile-numbers-box optimalization" :class="determineStyle(row.performance_info.Optimization)" title="optimalization">{{ row.performance_info.Optimization }}</div>
									<div>-</div>
									<div class="profile-numbers-box unknown" :class="determineStyle(row.performance_info.Unknown)" title="unknown">{{ row.performance_info.Unknown }}</div>
								</div>
							</div>
						</div>
						<div class="table-pagination" v-if="commitsFiltered.length">
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
									<span class="page-number" @click="currentPage = numberPages" v-model="commitsFiltered">{{ numberPages }}</span>
								</div>
								<div v-if="currentPage < numberPages" @click="currentPage++" v-model="commitsFiltered"><span>NEXT</span><span class="arrow hollow right"></span></div>
							</div>
						</div>
					</div>
				</template>
			</div>
		</div>
	</div>
</template>

<script type="text/javascript">
	export default {
		data: function() {
			return {
				tableCols: {
					minor_version: 'Minor version',
					message: 'Commit message',
					date: 'Date',
					profiles: 'Collected profiles',
					performance_info: 'Performance',
				},
				displayNumber: '',
				sortOrder: ['asc'],
				sortKey: ['name'],
				sortArrow: false,
				filterKey: '',
				currentPage: 1,
				numberPages: '',
				itemsPerPage: 5,
				userItemsPerPage: 5,
			}
		},
		created: function() {
			this.$store.dispatch({
				type: 'loadBranches', 
				path: this.$store.getters.currentRepoPath,
			});
			this.$store.dispatch({
				type: 'loadCommits', 
				path: this.$store.getters.currentRepoPath,
				branch: this.$store.getters.currentBranch,
			});
		},
		computed: {
			/**
			 * Gets current repository name from shared state
			 */
			currentRepoName: function() {
				return this.$store.getters.currentRepoName;
			},
			/**
			 * Gets current repository path from shared state
			 */
			currentRepoPath: function() {
				return this.$store.getters.currentRepoPath;
			},
			/**
			 * Gets list of branches from the shared state
			 */
			optionalBranches: function() {
				return this.$store.getters.optionalBranches;
			},
			/**
			 * Gets list of commits from the shared state
			 */
			tableRows: function() {
				return this.$store.getters.commits;
			},
			/**
			 * Fetches branch name and get it from the shared state
			 */
			currentBranch: {
				get: function() {
					return this.$store.getters.currentBranch;
				},
				set: function(value) {
					this.$store.dispatch({
						type: 'setCurrentBranch', 
						branch: value,
						path: this.currentRepoPath,
					});
				},
			},
			/**
			 * Filters list of displayed commits
			 */
			commitsFiltered: function () {
				var data = this.tableRows.filter((repo) => {
					var keys = Object.keys(repo);
					for (var i = 0; i < keys.length; i++) {
						if (keys[i] != 'performance_info' && keys[i] != 'profiles') {
							if (repo[keys[i]].match(this.filterKey)) {
								return true;
							}
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
			 * Sets sort order and sorting key
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
			 * Determines style of degradation boxes
			 */
			determineStyle: function(value) {
				return (value == 0 ? 'empty' : '');
			},
			/**
			 * Switches context to a single commit
			 */
			goTo: function(minor_version) {
				this.$router.push({ 
					name: 'commit',
					params: { 
						repo: this.currentRepoName,
						commit: minor_version.minor_version,
						originRepositoryPath: this.currentRepoPath,
				}});
			}
		},
	}
</script>


