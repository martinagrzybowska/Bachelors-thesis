<template>
	<div class="main-container">
		
		<sidebar :originRepositoryPath="originRepositoryPath"></sidebar>

		<div class="container">

			<transition name="fade">
				<mmodal v-show="isModalVisible" @close="closeModal"></mmodal>
			</transition>

			<div class="header-container">
				<div class="current-heading">
					<p>Minor version {{ this.$route.params.commit }}</p>
				</div>
				<div class="current-heading right">
					<p>repository <span>{{ this.$route.params.repo | capitalizeFirst }}</span></p>
				</div>
			</div>

			<div class="content-container">
				
				<div class="commit-information">
					<span>Commited by <b>{{ commitDetails.author }}</b> on {{ commitDetails.date }}</span>
					<span><i>"{{ commitDetails.message | capitalizeFirst }}"</i></span>
					
					<span v-if="countCommitParents(0)">This minor version has no parents</span>
					
					<span v-else-if="countCommitParents(1)">This minor version has 1 parent: 
						<b class="point" @click="goTo(commitDetails.parents[0])">{{ commitDetails.parents[0] }}</b>
					</span>
					
					<span v-else>This minor version has {{ commitDetails.parents.length }} parents: 
						<b class="point" v-for="(parent,index) in commitDetails.parents" @click="goTo(parent)">{{ parent }}
							<template v-if="index < commitDetails.parents.length - 1">, </template>
						</b>
					</span>
				</div>
				
				<profilesToggle :originRepositoryPath="originRepositoryPath"></profilesToggle>

				<div class="content-section-container collect">
					
					<div class="collect-container">
						
						<div>
							<span>Collect new performance profile using :</span>
						</div>
						
						<div class="collect-button table-button ">
							<div @click="showModal">
								<span>single job specification</span>
							</div>
							<div>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm144 276c0 6.6-5.4 12-12 12h-92v92c0 6.6-5.4 12-12 12h-56c-6.6 0-12-5.4-12-12v-92h-92c-6.6 0-12-5.4-12-12v-56c0-6.6 5.4-12 12-12h92v-92c0-6.6 5.4-12 12-12h56c6.6 0 12 5.4 12 12v92h92c6.6 0 12 5.4 12 12v56z"/></svg>
							</div>
						</div>
						
						<div class="collect-button table-button" @click="fireJobMatrix()">
							<div>
								<span>predefined job matrix</span>
							</div>
							<div>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm144 276c0 6.6-5.4 12-12 12h-92v92c0 6.6-5.4 12-12 12h-56c-6.6 0-12-5.4-12-12v-92h-92c-6.6 0-12-5.4-12-12v-56c0-6.6 5.4-12 12-12h92v-92c0-6.6 5.4-12 12-12h56c6.6 0 12 5.4 12 12v92h92c6.6 0 12 5.4 12 12v56z"/></svg>
							</div>
						</div>

					</div>

				</div>

			</div>
		</div>
	</div>
</template>

<script type="text/javascript">
	export default {
		data: function() {
			return {
				isModalVisible: false,
				originRepositoryPath: '',
				originBranch: '',
			}
		},
		watch: {
		    '$route.params.commit': function(to, from) {
		        this.$store.dispatch({
					type: 'loadCommitInfo',
					path: this.originRepositoryPath,
					commitId: this.$route.params.commit,
				});
		    }
		},
		created: function() {
			this.originRepositoryPath = this.$store.getters.currentRepoPath;
			this.originBranch = this.$store.getters.currentBranch;
			this.$store.dispatch({
				type: 'loadCommitInfo',
				path: this.originRepositoryPath,
				commitId: this.$route.params.commit,
			});
		},
		computed: {
			/**
			 * Gets current commit detailes from the shared state
			 */
			commitDetails: function() {	
				return this.$store.getters.commitInfo;
			},
			/**
			 * Sets current commit
			 */
			setCurrent: function() {
				this.currentCommit = this.$route.params.commit;
			},
		},
		methods: {
	    	/**
			 * Shows collection modal window
			 */
	    	showModal: function() {
	    		this.isModalVisible = true;
	    	},
	    	/**
			 * Hides collection modal window
			 */
	    	closeModal: function() {
	    		this.isModalVisible = false;
	    	},
	    	/**
			 * Determines the number of commits parents
			 */
	    	countCommitParents: function(value) {
	    		if (this.commitDetails.parents != undefined) {
	    			if (this.commitDetails.parents.length == value) {
	    				return true;
	    			}
	    		}
	    		return false;
	    	},
	    	/**
			 * Fires action for collecting profiles with specification
			 * (preparation for future development)
			 */
	    	/*collectNewProfile: function() {
				this.$store.dispatch({
					type: 'collectNewProfile',
					path: this.originRepositoryPath,
					commitId: this.$route.params.commit,
				});
			},*/
			/**
			 * Fires action for collecting new profiles based on the predefined job matrix
			 */
			fireJobMatrix: function() {
				this.$store.dispatch({
					type: 'collectNewProfileJobMatrix',
					path: this.originRepositoryPath,
					branch: this.originBranch,
					commitId: this.$route.params.commit,
				});
			},
			/**
			 * Switches context to another commit
			 * @param {string} commitId SHA of the commit
			 */
	    	goTo: function(commitId) {		
				this.$router.push({ 
					name: 'commit',
					params: { 
						repo: this.$route.params.repo, 
						commit: commitId, 
						originRepositoryPath: this.originRepositoryPath,
				}});
			},
	    },
	}
</script>










