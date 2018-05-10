<template>
	<div class="content-container">

		<template v-if="!registeredTableRows.length && !pendingTableRows.length">
			<smilingCookie><span slot="item">performance profiles</span></smilingCookie>
		</template>
		
		<template v-else>

			<div class="table-toggle-container">
				
				<div>
					<span>Show :</span>
				</div>
				
				<div class="table-toggle">
					<div class="table-toggle-item" v-for="(item, index) in toggleItems" 
						:key="'items' + index"
						:class="{ inactive: !item.active }" 
						@click=" item.active = !item.active; colsFiltered; rowsFiltered">
						<div>
							<span>{{ item.type }}</span>
						</div>
						<svg v-if="!item.active" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm144 276c0 6.6-5.4 12-12 12h-92v92c0 6.6-5.4 12-12 12h-56c-6.6 0-12-5.4-12-12v-92h-92c-6.6 0-12-5.4-12-12v-56c0-6.6 5.4-12 12-12h92v-92c0-6.6 5.4-12 12-12h56c6.6 0 12 5.4 12 12v92h92c6.6 0 12 5.4 12 12v56z"/></svg>
						
						<svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zM124 296c-6.6 0-12-5.4-12-12v-56c0-6.6 5.4-12 12-12h264c6.6 0 12 5.4 12 12v56c0 6.6-5.4 12-12 12H124z"/></svg>
					</div>
				</div>

			</div>

			<div class="content-section-container">
				<profileTable 
					:tableRows="registeredTableRowsFiltered" 
					:tableColsFirst="tableColsFirst" 
					:tableColsSecond="tableColsSecond" 
					:originCommit="setCurrent()" 
					heading="Registered performance profiles" 
					type="registered">
				</profileTable>
			</div>

			<div class="content-section-container">
				<profileTable 
					:tableRows="pendingTableRowsFiltered" 
					:tableColsFirst="tableColsFirst" 
					:tableColsSecond="tableColsSecond" 
					:originCommit="setCurrent()" 
					type="pending" 
					heading="Pending performance profiles">
				</profileTable>
			</div>

		</template>

	</div>
</template>

<script type="text/javascript">
	export default {
		data: function() {
			return {
				toggleItems: [
					{type: 'time', active: true},
					{type: 'command', active: true},
					{type: 'id', active: true},
					{type: 'profile type', active: true},
					{type: 'collector', active: true},
					{type: 'action', active: true},
				],

				tableCols: ['time','command', 'id', 'type','collector','action'],
				tableColsFirst: ['time','command', 'id'],
				tableColsSecond: ['type', 'collector','action'],

				currentCommit: '',
			}
		},
		created: function() {
			if (this.$route.params.commit == undefined) {
				this.fillToggle();
				this.$store.dispatch({
					type: 'loadRepoProfiles',
					path: this.originRepositoryPath,
				});
			}
			else {
				this.$store.dispatch({
					type: 'loadCommitProfiles',
					path: this.originRepositoryPath,
					commitId: this.$route.params.commit,
				});
			}
		},
		watch: {
		    '$route.params.commit': function(to, from) {
		        if (this.$route.params.commit == undefined) {
					this.fillToggle();
					this.$store.dispatch({
						type: 'loadRepoProfiles',
						path: this.originRepositoryPath,
					});
				}
				else {
					this.$store.dispatch({
						type: 'loadCommitProfiles',
						path: this.originRepositoryPath,
						commitId: this.$route.params.commit,
					});
				}
		    }
		},
		computed: {
			/**
			 * Gets current repository path from shared state
			 */
			originRepositoryPath: function() {
				return this.$store.getters.currentRepoPath;
			},
			/**
			 * Gets registered profiles reordered data
			 */
			registeredTableRows: function() {
				return this.changeOrder(this.$store.getters.registeredProfiles);
			},
			/**
			 * Gets pending profiles reordered data
			 */
			pendingTableRows: function() {
				return this.changeOrder(this.$store.getters.pendingProfiles);
			},
			/**
			 * Gets filtered registered profiles data
			 */
			registeredTableRowsFiltered: function() {
				return this.registeredTableRows;
			},
			/**
			 * Gets filtered pending profiles data
			 */
			pendingTableRowsFiltered: function() {
				return this.pendingTableRows;
			},
			/**
			 * Filters table col profiles
			 */
			colsFiltered: function () {
				var temp = 6;
				this.tableColsFirst = [];
				this.tableColsSecond = [];

				this.toggleItems.forEach(function(item){
					temp = item.active? temp : --temp;
				});

				this.toggleItems.forEach((item, index) =>  {
					if (temp/2 > this.tableColsFirst.length) {
						if (item.active) {
							this.tableColsFirst.push(this.tableCols[index]);
						}
					}
					else {
						if (item.active) {
							this.tableColsSecond.push(this.tableCols[index]);
						}
					}

				});
			},
			/**
			 * Filters table row profiles
			 */
			rowsFiltered: function() {
				Object.keys(this.registeredTableRows).forEach((item) => {
					
					if (this.tableColsFirst.includes(item) || this.tableColsSecond.includes(item)) {
						this.registeredTableRowsFiltered[item] = this.registeredTableRows[item];
					}
				});

				Object.keys(this.pendingTableRows).forEach((item) => {
					if (this.tableColsFirst.includes(item) || this.tableColsSecond.includes(item)) {
						this.pendingTableRowsFiltered[item] = this.pendingTableRows[item];
					}
				})
			},
		},
		methods: {
			/**
			 * Sets current commit
			 */
			setCurrent: function() {
				return this.$route.params.commit;
			},
			/**
			 * Fills toggle panel with data
			 */
			fillToggle: function() {
				this.toggleItems.splice(3,1);
				this.tableCols.splice(3,1);
				this.tableColsSecond.splice(0,1);
				
				this.toggleItems.unshift({type: 'commit', active: true});
				this.toggleItems.unshift({type: 'branch', active: true});
				this.tableCols.unshift('commit');
				this.tableCols.unshift('branch');
				console.log()
				this.tableColsFirst = this.tableCols.slice(0, 3);
				this.tableColsSecond = this.tableCols.slice(3);
			},
			/**
			 * Change order of profile data
			 */
			changeOrder: function(toOrder) {
	    		var tmp = [];
	    		if (this.$route.params.commit == undefined) {
	    			var order = ["branch","commit","id", "time","command","collector","type","action","path"];
	    		}
	    		else {
	    			var order = ["time","command", "id","type","collector","action","path"];
	    		}
	    		toOrder.forEach((item) => {
	    			tmp.push(JSON.parse(JSON.stringify(item, order , 0)));
	    		});
	    		return tmp;
	    	},
		}, 
	}
</script>