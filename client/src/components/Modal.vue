<template>
	<transition name="custom-modal-fade">
		<div class="custom-modal-backdrop" @click.self="close()">
			
			<div class="custom-modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
				
				<div class="custom-modal-header" id="modalTitle">
					<div><slot name="header">Single Job Specification</slot></div>
					<svg @click="close" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
				</div>
				
				<div class="custom-modal-body" id="modalDescription">
					
					<collectionSettings v-if="!previewActive" 
						:modalProfiledCommands="singleJobSpecification.profiledCommands" 
						:modalCollectionSpecification="singleJobSpecification.collectionSpecification" 
						mode="modal">
					</collectionSettings>

					<div v-else class="preview">
						
						<table class="table-container table">
							
							<thead class="table-header">
								<tr>
									<th class="table-header-item" v-for="col in tableCols" :key="col">
										<span>{{ col }}</span>
									</th>
								</tr>
							</thead>
							
							<tbody class="table-body">
								
								<tr class="table-body-row" v-for="(row, index) in tableRows" :key="index">
									<td class="table-body-row-item" v-for="cell in row">
										
										<template v-if="!cell.name">
											<span>{{ cell }}</span>
										</template>
										
										<template v-else>
											<div>
												<span class="collection-item-heading">name:</span>
												<span class="collection-item-content">{{ cell.name }}</span><br>
												
												<template v-for="(param, index) in cell.parameters">
													
													<span class="collection-item-heading" :key="'heading' + index">param:</span>
													<span class="collection-item-content" :key="'value' + index">{{ param.param }}   </span>
													
													<template v-if="param.options.length">
														<span class="collection-item-heading">options:</span>
														<span v-for="(option, index) in param.options" :key="'preview' + option + index" class="collection-item-content">{{ option }}</span>
													</template>
													<br>

												</template>
											</div>
										</template>

									</td>
								</tr>

							</tbody>

						</table>
						
						<span class="no-combinations" v-if="!tableRows"> No combinations to display</span>
					
					</div>
				</div>
				
				<div class="custom-modal-footer">
					
					<div class="table-button" @click="collectNewProfile()">
						<span>collect</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z"/></svg>
					</div>
					
					<div class="table-button reload" @click="previewActive = !previewActive">
						<template v-if="!previewActive">
							<span>preview</span>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M569.354 231.631C512.969 135.949 407.81 72 288 72 168.14 72 63.004 135.994 6.646 231.631a47.999 47.999 0 0 0 0 48.739C63.031 376.051 168.19 440 288 440c119.86 0 224.996-63.994 281.354-159.631a47.997 47.997 0 0 0 0-48.738zM288 392c-75.162 0-136-60.827-136-136 0-75.162 60.826-136 136-136 75.162 0 136 60.826 136 136 0 75.162-60.826 136-136 136zm104-136c0 57.438-46.562 104-104 104s-104-46.562-104-104c0-17.708 4.431-34.379 12.236-48.973l-.001.032c0 23.651 19.173 42.823 42.824 42.823s42.824-19.173 42.824-42.823c0-23.651-19.173-42.824-42.824-42.824l-.032.001C253.621 156.431 270.292 152 288 152c57.438 0 104 46.562 104 104z"/></svg>
						</template>
						<template v-else>
							<span>specify</span>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M8 256c0 137 111 248 248 248s248-111 248-248S393 8 256 8 8 119 8 256zm448 0c0 110.5-89.5 200-200 200S56 366.5 56 256 145.5 56 256 56s200 89.5 200 200zm-72-20v40c0 6.6-5.4 12-12 12H256v67c0 10.7-12.9 16-20.5 8.5l-99-99c-4.7-4.7-4.7-12.3 0-17l99-99c7.6-7.6 20.5-2.2 20.5 8.5v67h116c6.6 0 12 5.4 12 12z"/></svg>
						</template>
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

<script>
	export default {
		data: function() {
			return {
				singleJobSpecification: {
					profiledCommands: {
						commands: [''],
						arguments: [''],
						workload: [''],
					},
					collectionSpecification: {
						collectors: [
							{ name: '', parameters: [ { param: '', options: [''] } ] },
						],
						postprocessors: [
							{ name: '', parameters: [ { param: '', options: [''] } ] },
						],
					},
				},
				tableCols: [
					'command', 'argument', 'workload', 'collector', 'postprocessor'
				],
				previewActive: false,
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
			 * Creates a preview of combinations of all input values for subsequent profile collection
			 */
			tableRows: function() {
				var row;
				var table = [];
				this.singleJobSpecification.profiledCommands.commands.forEach(command => {
					this.singleJobSpecification.profiledCommands.arguments.forEach(arg => {
						this.singleJobSpecification.profiledCommands.workload.forEach(load => {
							this.singleJobSpecification.collectionSpecification.collectors.forEach(collector => {
								this.singleJobSpecification.collectionSpecification.postprocessors.forEach(processor => {
									if (collector.name == '' && processor.name == '') {
										row = [command, arg, load, '', ''];
									}
									else if (collector.name == '') {
										row = [command, arg, load, '', processor];
									}
									else if (processor.name == '') {
										row = [command, arg, load, collector, ''];
									}
									else {
										row = [command, arg, load, collector, processor];
									}
									table.push(row);
								});
							});
						});
					});
				});

				for (var iter = 0; iter < table.length; iter++) {
					for (var i = 0; i < table[iter].length; i++) {
						if (table[iter][i] != '') {
							return table;
						}
					}
				}
				return '';
			}
		},
		methods: {
			/**
			 * Close event
			 * @event close
			 */
			close: function() {
				this.$emit('close');
			},
			/**
			 * Fires action for collecting new profiles based on the input specification, currently under development
			 */
			collectNewProfile: function() {
				this.$store.dispatch({
					type: 'collectNewProfile',
					path: this.originRepositoryPath,
					commitId: this.$route.params.commit,
					specification: this.singleJobSpecification,
				});
				this.close();
			},
		},
	};
</script>

<style scoped>

.table-header .table-header-item {
	text-align: center;
}

.table-header th {
	border-top: none!important;
	border-bottom: 2px solid #dbe6ec!important;
}

.table-header .table-header-item span {
	color: #768389;
	font-size: 12px;
	font-weight: 400;
	text-transform: uppercase;
}

.table-body-row-item>span {
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	word-wrap: normal;
	color: #585c5e;
		font-weight: 400;
	display: inline-block;
	font-size: 13px;
	vertical-align: center;
	padding: auto;
}

.table-body-row-item div {
	text-align: left;
	padding: 5px 15px;
}
.table-body {
	border-bottom: 2px solid #dbe6ec!important;
	width: 100%;
}

.table-body-row:nth-child(odd) {
	background-color: #f4f9f9!important;
}

.table td:nth-child(4) {
	border-right: 1px solid #dbe6ec;
	border-left: 1px solid #dbe6ec;
	width: 300px;
}

.collection-item-heading {
	color: #768389;
	font-size: 12px!important;
	font-weight: 400;
	text-transform: uppercase;
}
.collection-item-content {
	color: #768389;
	font-size: 12px!important;
	font-weight: 300;
	padding-right: 10px;
}

.no-combinations {
	width: 100%;
	display: block;
	text-align: center;
	color: #768389;
	font-size: 13px!important;
	font-style: italic;
	font-weight: 200;
	padding-bottom: 15px;
	border-bottom: 2px solid #dbe6ec;
}

.table > tbody > tr > td {
 	vertical-align: middle;
	padding: 0!important;
	text-align: center;
}

.table > tbody > tr > td > span {
	vertical-align: middle;
	padding: 10px 0;
}

</style>