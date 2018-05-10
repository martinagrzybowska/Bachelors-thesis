<template>
	<div class="side-bar">	
		<div class="side-bar-nav-container">
			
			<div class="aside" @click="goTo('dashboard')" :class="{active: isActive('dashboard')}">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M500 400c6.6 0 12 5.4 12 12v24c0 6.6-5.4 12-12 12H12c-6.6 0-12-5.4-12-12V76c0-6.6 5.4-12 12-12h24c6.6 0 12 5.4 12 12v324h452zm-356-60v-72c0-6.6-5.4-12-12-12h-24c-6.6 0-12 5.4-12 12v72c0 6.6 5.4 12 12 12h24c6.6 0 12-5.4 12-12zm96 0V140c0-6.6-5.4-12-12-12h-24c-6.6 0-12 5.4-12 12v200c0 6.6 5.4 12 12 12h24c6.6 0 12-5.4 12-12zm96 0V204c0-6.6-5.4-12-12-12h-24c-6.6 0-12 5.4-12 12v136c0 6.6 5.4 12 12 12h24c6.6 0 12-5.4 12-12zm96 0V108c0-6.6-5.4-12-12-12h-24c-6.6 0-12 5.4-12 12v232c0 6.6 5.4 12 12 12h24c6.6 0 12-5.4 12-12z"/></svg>
				<span>Dashboard</span>
			</div>

			<div class="aside" @click="goTo('minor-versions')" :class="{active: isActive('minor-versions')}">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="50%" height="50%"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200z"/></svg>
				<span>Minor Versions</span>
			</div>

			<div class="aside" @click="goTo('performance-profiles')" :class="{active: isActive('performance-profiles')}">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M500 384c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12H12c-6.6 0-12-5.4-12-12V76c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v308h436zM456 96H344c-21.4 0-32.1 25.9-17 41l32.9 32.9-72 72.9-55.6-55.6c-4.7-4.7-12.2-4.7-16.9 0L96.4 305c-4.7 4.6-4.8 12.2-.2 16.9l28.5 29.4c4.7 4.8 12.4 4.9 17.1.1l82.1-82.1 55.5 55.5c4.7 4.7 12.3 4.7 17 0l109.2-109.2L439 249c15.1 15.1 41 4.4 41-17V120c0-13.3-10.7-24-24-24z"/></svg>
				<span>Performance Profiles</span>
			</div>

			<div class="aside" @click="goTo('local-settings')" :class="{active: isActive('local-settings')}">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M444.788 291.1l42.616 24.599c4.867 2.809 7.126 8.618 5.459 13.985-11.07 35.642-29.97 67.842-54.689 94.586a12.016 12.016 0 0 1-14.832 2.254l-42.584-24.595a191.577 191.577 0 0 1-60.759 35.13v49.182a12.01 12.01 0 0 1-9.377 11.718c-34.956 7.85-72.499 8.256-109.219.007-5.49-1.233-9.403-6.096-9.403-11.723v-49.184a191.555 191.555 0 0 1-60.759-35.13l-42.584 24.595a12.016 12.016 0 0 1-14.832-2.254c-24.718-26.744-43.619-58.944-54.689-94.586-1.667-5.366.592-11.175 5.459-13.985L67.212 291.1a193.48 193.48 0 0 1 0-70.199l-42.616-24.599c-4.867-2.809-7.126-8.618-5.459-13.985 11.07-35.642 29.97-67.842 54.689-94.586a12.016 12.016 0 0 1 14.832-2.254l42.584 24.595a191.577 191.577 0 0 1 60.759-35.13V25.759a12.01 12.01 0 0 1 9.377-11.718c34.956-7.85 72.499-8.256 109.219-.007 5.49 1.233 9.403 6.096 9.403 11.723v49.184a191.555 191.555 0 0 1 60.759 35.13l42.584-24.595a12.016 12.016 0 0 1 14.832 2.254c24.718 26.744 43.619 58.944 54.689 94.586 1.667 5.366-.592 11.175-5.459 13.985L444.788 220.9a193.485 193.485 0 0 1 0 70.2zM336 256c0-44.112-35.888-80-80-80s-80 35.888-80 80 35.888 80 80 80 80-35.888 80-80z" /></svg>
				<span>Local Settings</span>
			</div>
		
		</div>

	</div>
</template>

<script type="text/javascript">
	export default {
		created: function() {

			var temp = this.$route.path.slice(1);
			temp = temp.slice(temp.indexOf('/') + 1);

			if (temp.match('dashboard')) {
				this.activeItem = 'dashboard';
			}
			else if (temp.match('performance-profiles')) {
				this.activeItem = 'performance-profiles';
			}
			else if (temp.match('minor-versions')) {
				this.activeItem = 'minor-versions';
			}
			else {
				this.activeItem = 'local-settings';
			}
		},

		data: function () {
			return {
				activeItem: '',
			}
		},
		computed: {
			originRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			},
		},
		methods: {
			/**
			 * Determines whether the item is active
			 * @param {string} item to check
			 */
			isActive: function(item) {
				return this.activeItem == item;
			},
			/**
			 * Switch context to another location
			 * @param {string} location to go to
			 */
			goTo: function(location) {
				this.$router.push({ 
					name: location, 
					params: { repo: this.$route.params.repo, originRepositoryPath: this.originRepositoryPath,
				}});
			}
		},
	}

</script>

<style scoped>

.main-container .side-bar {
	flex: 0 0 100px;
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	background-color: #f4f9f9;
	border-right: 1px solid #e3e8e8;
}

.side-bar .side-bar-nav-container {
	display: flex;
	flex-direction: column;
	flex: 0 1 auto;
	margin-top: 25px;
}

.side-bar .aside {
	flex: 0 1 85px;
	
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	cursor: pointer;
	
	color: #455A64;
	text-decoration: none;
	font-size: 11px;
	margin: 5px 0;
}

.side-bar .side-bar-nav-container .aside>span {
	margin: 8px 5px;
	width: 70%;
	text-align: center;
}

.side-bar .aside>svg {
	width: 20px;
	height: 20px;
	text-align: center;
	padding: auto;
	fill: #546E7A;
}

.side-bar .side-bar-nav-container .aside {
	position: relative;
	cursor: pointer;
}

.side-bar .side-bar-nav-container .aside:hover {
	cursor: pointer;
	color: #263238;
}

.side-bar .aside:hover svg, .aside.active svg {
	fill: #26A69A;
	font-weight: bold;
	cursor: pointer;
}

.aside.active:after {
	width: 0;
    height: 0;
    border-top: 9px solid transparent;
    border-bottom: 9px solid transparent;
    display: block;
    content: "";
    position: absolute;
    top: 25px;
    right: 0;
    margin-right: -1px;
    border-right: 9px solid white;
}

.aside.active:before {
	width: 0;
    height: 0;
    border-top: 11px solid transparent;
    border-bottom: 11px solid transparent;
    display: block;
    content: "";
    position: absolute;
    top: 23px;
    right: 0;
    margin-right: -1px;
    border-right: 11px solid #e3e8e8;
    z-index: 0;
}

</style>