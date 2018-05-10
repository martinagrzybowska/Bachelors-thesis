<template>
	<div class="main-container">

		<transition name="fade">
			<removeModal v-show="isRemoveModalVisible" @close="closeModal" @confirm="removeRepo()">
				<span slot="header">Do you really wish to remove the Perun wrapper over the repository <b>{{ this.$route.params.repo | capitalizeFirst }}</b>?</span>
			</removeModal>
		</transition>

		<sidebar></sidebar>
		
		<div class="container">
			
			<div class="header-container">
				<div class="current-heading right">
					<p>repository <span>{{ this.$route.params.repo | capitalizeFirst }}</span></p>
				</div>
			</div>
			
			<div class="content-container">
				
				<div class="dashboard-container">
					
					<div class="dashboard-repo-info-wrapper">
						
						<div class="dashboard-repo-info">
							
							<div>
								<span class="heading">Perun wrapper is currently</span>
							</div>
							
							<div>
								<div class="profile-origin-buttons">
									<div class="table-button register">
										<span>active</span>
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z"/></svg>
									</div>
									<div class="table-button remove" @click="showModal()">
										<span>remove</span>
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
									</div>
								</div>
							</div>

						</div>
						
						<div class="dashboard-repo-path">
							<div>
								<span class="heading">Path to repository is</span>
							</div>
							<div>
								<span>{{ originRepositoryPath }}</span>
							</div>
						</div>

					</div>

					<template v-if="!tableRows.length">
						<smilingCookie><span slot="item">stats</span></smilingCookie>
					</template>
					
					<template v-else>
						
						<template v-if="profileNumbers.all == 0">
							<smilingCookie><span slot="item">performance profile stats</span></smilingCookie>
						</template>
						<template v-else>
							<div class="dashboard-row">
								<div class="dashboard-row-column tiles">
									
									<div class="dashboard-profile-tile">
										
										<div class="tile-upper-part all">
											<div class="wrap">
												<span class="number"><animateNumber :number="profileNumbers.all"></animateNumber></span>
												<div>
													<span class="heading">total</span>
													<span>profiles</span>
												</div>
											</div>
										</div>
										
										<div class="tile-lower-part all"></div>

									</div>
									
									<div class="dashboard-profile-tile">
										<div class="tile-upper-part mixed">
											<div class="wrap">
												<span class="number"><animateNumber :number="profileNumbers.mixed"></animateNumber></span>
												<div>
													<span class="heading">mixed</span>
													<span>profiles</span>
												</div>
											</div>
										</div>
										<div class="tile-lower-part mixed"></div>
									</div>
									
									<div class="dashboard-profile-tile">
										<div class="tile-upper-part time">
											<div class="wrap">
												<span class="number"><animateNumber :number="profileNumbers.time"></animateNumber></span>
												<div>
													<span class="heading">time</span>
													<span>profiles</span>
												</div>
											</div>
										</div>
										<div class="tile-lower-part time">
										</div>
									</div>
									
									<div class="dashboard-profile-tile">
										<div class="tile-upper-part memory">
											<div class="wrap">	
												<span class="number"><animateNumber :number="profileNumbers.memory"></animateNumber></span>
												<div>
													<span class="heading">memory</span>
													<span>profiles</span>
												</div>
											</div>
										</div>
										<div class="tile-lower-part memory"></div>
									</div>

								</div>
								
								<div class="dashboard-row-column tiles chart-wrapper">
									<highcharts :options="options" ref="highcharts"></highcharts>
								</div>

							</div>
						</template>
				
						<div class="dashboard-row">
							<div class="main-table dashboard table-div table-striped table--striped table--md">
								
								<div class="table-header">
									<div class="row">
										<div class="table-head align-left col-lg-2">BRANCH NAME</div>
										<div class="table-head align-left col-lg-2">HEAD</div>
										<div class="table-head align-left col-lg-2">PERFORMANCE PROFILES</div>
										<div class="table-head align-left col-lg-6">PROFILES DEGRADATION</div>		
									</div>
								</div>

								<div class="table-body text-center">
									<div class="row table-row" v-for="row in tableRows" :key="row.id">
										
										<div class="col-lg-2 align-left" @click="goTo(row)">
											<div class="commit-head-box" v-if="row.checkout">HEAD</div>
											<span>{{ row.branch }}</span>
										</div>
										
										<div class="col-lg-2 align-left" @click="goTo(row)">
											<span>{{ row.commit }}</span>
										</div>
										
										<div class="col-lg-2 align-left">
											<div class="profile-numbers-box time" :class="determineStyle(row.profiles.time)" title="time">{{ row.profiles.time }}</div>
											<div class="profile-numbers-box memory" :class="determineStyle(row.profiles.memory)" title="memory">{{ row.profiles.memory }}</div>
											<div class="profile-numbers-box mixed" :class="determineStyle(row.profiles.mixed)" title="mixed">{{ row.profiles.mixed }}</div>
											<span class="dash">-</span>
											<div class="profile-numbers-box all" :class="determineStyle(row.profiles.all)" title="all">{{ row.profiles.all }}</div>
										</div>
										
										<div class="col-lg-6 align-left dashboard-table-profiles degradation-info">
											<span>DEG:</span>
											<div class="profile-numbers-box degradation" :class="determineStyle(row.performance.Degradation)" title="degradation">{{ row.performance.Degradation }}</div>
											
											<span>MAYBE DEG:</span>
											<div class="profile-numbers-box maybe-degradation" :class="determineStyle(row.performance.MaybeDegradation)" title="maybe-degradation">{{ row.performance.MaybeDegradation }}</div>
											
											<span>NO CHANGE:</span>
											<div class="profile-numbers-box no-change" :class="determineStyle(row.performance.NoChange)" title="no-change">{{ row.performance.NoChange }}</div>
											
											<span>MAYBE OPT:</span>
											<div class="profile-numbers-box maybe-optimalization" :class="determineStyle(row.performance.MaybeOptimization)" title="maybe-optimalization">{{ row.performance.MaybeOptimization }}</div>
											
											<span>OPT:</span>
											<div class="profile-numbers-box optimalization" :class="determineStyle(row.performance.Optimization)" title="optimalization">{{ row.performance.Optimization }}</div>
											
											<span class="dash">-</span>
											
											<span>UNKNOWN:</span>
											<div class="profile-numbers-box unknown" :class="determineStyle(row.performance.Unknown)" title="unknown">{{ row.performance.Unknown }}</div>
										</div>

									</div>
								</div>

							</div>
						</div>
					</template>

				</div>
			</div>
		</div>
	</div>
</template>

<script type="text/javascript">
	/* Custom component used for animating numbers */
	import AnimateNumber from './AnimateNumber';
	export default {
		components: {
			animateNumber: AnimateNumber,
		},
		data: function() {
			return {
				isRemoveModalVisible: false,
			}
		},
		created: function() {
			this.$store.dispatch({
				type: 'loadDashboard',
				path: this.originRepositoryPath,
			});
		},
		methods: {
			/**
			 * Shows the remove modal window
			 */
			showModal: function() {
				this.isRemoveModalVisible = true;
			},
			/**
			 * Closes the remove modal window
			 */
			closeModal: function() {
				this.isRemoveModalVisible = false;
			},
			/**
			 * Determines the style of profile box in table
			 */
			determineStyle: function(value) {
				return (value == 0 ? 'empty' : '');
			},
			/**
			 * Fires action for removing Perun instance
			 */
			removeRepo: function() {	
				this.$store.dispatch({
					type: 'removeRepoIntegration',
					path: this.originRepositoryPath,
				})
				this.closeModal();
				this.$router.replace('/');
			},
			/**
			 * Switches context to a single commit
			 */
			goTo: function(row) {
				this.$router.push({ 
					name: 'commit',
					params: { 
						repo: this.$route.params.repo,
						commit: row.commit,
						originRepositoryPath: this.originRepositoryPath,
				}});
			},
		},
		computed: {
			/**
			 * Gets dashboard tiles data from the shared state
			 */
			profileNumbers: function() {
				return this.$store.getters.dashboard.all;
			},
			/**
			 * Gets current repository path from shared state
			 */
			originRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			},
			/**
			 * Gets branches data from the shared state
			 */
			tableRows: function() {
				return this.$store.getters.dashboard.branches;
			},
			/**
			 * Determines and displays the dashboart chart data
			 */
			options: function(){
				return { 
					chart: {
						plotBackgroundColor: null,
						plotBorderWidth: null,
						plotShadow: false,
						type: 'pie',
						height: '240px',
					},
					legend: {
					    align: 'bottom',
					    layout: 'horizontal',
					    verticalAlign: 'bottom',
					    x: 145,
					    y: 0,
					},
					title: {
						text: ''
					},
					tooltip: {
						pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
					},
					plotOptions: {
						pie: {
							allowPointSelect: true,
							cursor: 'pointer',
							dataLabels: {
								enabled: true,
								format: '<b>{point.name}</b>: {point.percentage:.1f} %',
							},
							showInLegend: true,
							startAngle: -90,
					        endAngle: 90,
					        center: ['50%', '75%'],
						},
					},
					credits: false,
					series: [{
						name: 'Brands',
						type: 'pie',
						allowPointSelect: true,
						innerSize: '50%',
						colorByPoint: true,
						data: [
						{
							name: 'mixed',
							y: (this.profileNumbers.mixed * 100)/this.profileNumbers.all,
							color: '#42A5F5',
						}, 
						{
							name: 'memory',
							y: (this.profileNumbers.memory * 100)/this.profileNumbers.all,
							color: '#009688',
						}, 
						{
							name: 'time',
							y: (this.profileNumbers.time * 100)/this.profileNumbers.all,
							color: '#26C6DA',
						}]
					}]
				}
			}
		},
	}

</script>
