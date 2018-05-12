<template>
	<div>
		<div class="profile-visualization-container">
			
			<div class="profile-visualization-item dropdown ending">
				<select v-model="selectedGraph" @change="selectChartType(selectedGraph)">
					<option disabled value="">Please select one</option>
					<option v-for="type in graphTypes">{{ type }}</option>
				</select>
			</div>
			
			<div class="profile-visualization-item">
				<span>displaying</span>
			</div>
			
			<div class="profile-visualization-item dropdown y-axis">
				<select v-model="selectedOptions.y">
					<option disabled value="">Please select one</option>
					<option selected>{{ selectedOptions.y }}</option>
					<template v-for="type in availableNumericalOptions">
						<option v-if="checkOptionAvailability(type, 'y')" :key="'y' + type" :value="type">{{ type }}</option>
					</template>
				</select>
			</div>
			
			<div class="profile-visualization-item">
				<span>depending on</span>
			</div>

			<div v-if="selectedGraph != 'scatter'" class="profile-visualization-item dropdown" :class="selectedGraph != 'scatter'? 'ending': ''">
				<select v-model="selectedOptions.x">
					<option disabled value="">Please select one</option>
					<option selected>{{ selectedOptions.x }}</option>
					<template v-for="type in availableChartOptions">
						<option v-if="checkOptionAvailability(type, 'x')" :key="'xnormal' + type" :value="type">{{ type }}</option>
					</template>
				</select>
			</div>
			<div v-else class="profile-visualization-item dropdown" :class="selectedGraph != 'scatter'? 'ending': ''">
				<select v-model="selectedOptions.x">
					<option disabled value="">Please select one</option>
					<option selected>{{ selectedOptions.x }}</option>
					<template v-for="type in availableNumericalOptions">
						<option v-if="checkOptionAvailability(type, 'x')" :value="type" :key="'xscatter' + type">{{ type }}</option>
					</template>
				</select>
			</div>

			<template v-if="selectedGraph != 'scatter'">
			
				<div class="profile-visualization-item">
					<input type="radio" :name="profileName" value="none" v-model="selectedOptions.type">
					<span>none</span>
				</div>
				
				<div class="profile-visualization-item">
					<input type="radio" :name="profileName" value="stacked" v-model="selectedOptions.type">
					<span>stacked</span>
				</div>
				
				<div v-if="selectedGraph == 'bar'" class="profile-visualization-item">
					<input type="radio" :name="profileName" value="grouped" v-model="selectedOptions.type">
					<span>grouped</span>
				</div>
				<div v-else-if="selectedGraph == 'flow'" class="profile-visualization-item">
					<input type="radio" :name="profileName" value="accumulated" v-model="selectedOptions.type">
					<span>accumulated</span>
				</div>
				
				<div class="profile-visualization-item">
					<span>by</span>
				</div>
				
				<div v-if="selectedOptions.type != 'none'" class="profile-visualization-item dropdown ending">
					<select v-model="selectedOptions.by">
						<option disabled value="">Please select one</option>
						<option selected>{{ selectedOptions.by }}</option>
						<template v-for="type in availableChartOptions">
							<option v-if="checkOptionAvailability(type, 'by')" :value="type" :key="'by' + type">{{ type }}</option>
						</template>
					</select>
				</div>
				
				<div v-else-if="checkSwitchToNone()" class="profile-visualization-item dropdown ending" >
					<select>
						<option selected>{{ selectedOptions.by }}</option>
					</select>
				</div>
				
				<div class="profile-visualization-item">
					<span>aggregated by</span>
				</div>
				
				<div class="profile-visualization-item dropdown">
					<select v-model="selectedOptions.func">
						<option disabled value="">Please select one</option>
						<option v-for="type in aggregationTypes">{{ type }}</option>
					</select>
				</div>

			</template>
		</div>

		<div class="graph-container">
			<highcharts :options="options" ref="highcharts"></highcharts>
		</div>

	</div>
</template>

<script type="text/javascript">
	export default {
		props: {
			chartData: {
				type: Object,
				required: true,
				default: () => ({}),
			},
			originalOptions: {
				type: Object,
				required: true,
				default: () => ({}),
			},
			originalNumericalOptions: {
				type: Object,
				required: true,
				default: () => ({}),
			},
			profileName: {
				type: String,
				required: true,
				default: () => (""),
			},
		},
		data: function() {
			return {
				from_server: [
					{amount: 18, uid: 'ahoj', cluster: 19},
					{amount: 8, uid: 'bla', cluster: 19},
					{amount: 17, uid: 'ahoj', cluster: 13},
					{amount: 13, uid: 'ahoj', cluster: 19},
					{amount: 2, uid: 'bla', cluster: 12},
				],
				categoriesNum: 0,
				selectedGraph: 'bar',
				previousGraphType: 'none',
				graphTypes: [
					'bar', 'flow', 'scatter'
				],
				selectedOptions: {
					'x': 'uid',
					'y': 'amount',
					'type': 'none',
					'by': '----',
					'func': 'none',
				},
				selectedAggregation: 'none',
				aggregationTypes: [
					'none',
					'sum',
					'mean',
					'count',
					'median',
					'min',
					'max',
				],
			}
		},
		computed: {
			/**
			 * Returns a copy of original options for axis'
			 */
			availableChartOptions: function() {
				return this.originalOptions.slice();
			},
			/**
			 * Returns a copy of original numerical options for axis'
			 */
			availableNumericalOptions: function() {
				return this.originalNumericalOptions.slice();
			},
			/**
			 * Transforms chart names into highcharts chart types
			 */
			chartType: function() {
				if (this.selectedGraph == 'bar') {
					return 'column';
				}
				else if (this.selectedGraph == 'flow') {
					if (this.selectedOptions.type == 'stacked') {
						return 'area';
					}
					else {
						return '';
					}
				}
				else if (this.selectedGraph == 'scatter') {
					return 'scatter';
				}
			},
			/**
			 * Returns chart specification in Highcharts format
			 */
			options: function() {
				if (this.chartData != undefined) {
					var output = {	
						chart: {
					        type: this.chartType,
					        zoomType: "xy",
					    },
					    credits: false,
					    title: {
					        text: '',
					    },
					    xAxis: {
					        crosshair: true,
					        categories: this.fillCategories(),
					        min: 0,
					        max: this.categoriesNum,
					        title: {
					        	text: this.selectedOptions.x,
					        },
					    },
					    plotOptions: {
					        column: {
					            stacking: this.selectedOptions.type == 'stacked' ? 'normal' : '',
					        },
					        area: {
					            stacking: 'normal',
					            lineColor: '#666666',
					            lineWidth: 1,
					            marker: {
					                lineWidth: 1,
					                lineColor: '#666666'
					            }
					        }
					    },
					    yAxis: {
					        title: {
					            text: this.selectedOptions.y,
					        },
					    },
					    series: this.getChartSeries,
					}
					return output;
				}
				return {};
			},
			/**
			 * Calculates Highcharts data from input data depending on the user-selected options
			 */
			getChartSeries: function() {
				var series = []

				if (Object.keys(this.chartData).length !== 0 || this.chartData.constructor !== Object) { 
		
					if (this.selectedOptions.x != '----' && this.selectedOptions.y != '----') {
						
						const json_groupBy = require('json-groupby');
						
						if (this.selectedGraph == 'bar' || this.selectedGraph == 'flow') {
							if (this.selectedOptions.type == 'none' || this.selectedOptions.by == '----') {
								var grouped = json_groupBy(this.chartData, [this.selectedOptions.x], [this.selectedOptions.y]);
								series = [{ data: this.getChartNone(grouped), showInLegend: false}];
							}
							else {
								var grouped = json_groupBy(this.chartData, [this.selectedOptions.by, this.selectedOptions.x], [this.selectedOptions.y]);
								series = this.getStackedGroupedBy(grouped);
							}
						}
						else {
							series = [{ data: []}]
							this.chartData.forEach((item) => {
								series[0].data.push([parseFloat(item[this.selectedOptions.x]), parseFloat(item[this.selectedOptions.y])])
							});
							series[0]['showInLegend'] = false;
						}
					}
				}

				return series
			},
		},
		methods: {
			/**
			 * Clears 'by option' if graph type switched to none
			 */
			checkSwitchToNone: function() {
				if (this.selectedOptions.type == 'none') {
					this.selectedOptions.by = '----';
					return true;
				}

				return false;
			},
			/**
			 * Creates a set up of options for different chart types
			 */
			selectChartType: function(chartType) {
				if (chartType == 'scatter') {
					this.selectedOptions.type = "none";
					this.selectedOptions.by = '----';
					if (this.originalNumericalOptions.length > 1) {
						this.selectedOptions.y = this.originalNumericalOptions[0];
						this.selectedOptions.x = this.originalNumericalOptions[1];
					}
					else {
						this.selectedOptions.y = '----';
						this.selectedOptions.x = '----';
					}
				}
				else {
					this.selectedOptions.type = "none";
					this.selectedOptions.by = "----";
				}
			},
			/**
			 * Determines which options are available for user to choose from
			 */
			checkOptionAvailability: function(value, type) {
				if (this.selectedOptions.x != value &&
					this.selectedOptions.y != value &&
					this.selectedOptions.by != value){
					
					return true;

				}

				if (value == '----') {
					if (type == 'x' && this.selectedOptions.x == '----') {
						return false;
					}
					else if (type == 'y' && this.selectedOptions.y == '----') {
						return false;
					}
					else if (type == 'by' && this.selectedOptions.by == '----') {
						return false;
					}
					return true;
				}
				
				if (this.selectedOptions.type == 'none') {
					if (this.selectedOptions.by == value) {
						this.selectedOptions.by == '----';
						return true;
					}
				}

				return false;
			},
			/**
			 * Determines the descriptions of X axis
			 */
			fillCategories: function() {
				var output = [];
				if (Object.keys(this.chartData).length !== 0 || this.chartData.constructor !== Object) { 
					if (this.selectedOptions.x != '----' && this.selectedOptions.y != '----') {
						const json_groupBy = require('json-groupby');
						if (this.selectedGraph != 'scatter') {
							var grouped = json_groupBy(this.chartData, [this.selectedOptions.x]);
							Object.keys(grouped).forEach((xValue) => {
								output.push(xValue);
							});
						}
						else {
							Object.keys(this.chartData).forEach((xValue) => {
								output.push(xValue[this.selectedOptions.x]);
							});
						}
					}
				}

				this.categoriesNum = output.length - 1;
				return output;

			},
			/**
			 * Creates a normal chart data depending on the grouped options
			 * @param {Object} grouped object holding grouped data
			 */
			getChartNone: function(grouped) {
				var output = []
				Object.keys(grouped).forEach((xValue) => {
					output.push(this.determineAction(grouped[xValue][this.selectedOptions.y].map(parseFloat)));
				})
				return output;
			},
			/**
			 * Creates a stacked chart data depending on the grouped options
			 * @param {Object} grouped object holding grouped data
			 */
			getStackedGroupedBy: function(grouped) {
				var output = []
				Object.keys(grouped).forEach((byValue) => {
					var yValues = this.getChartNone(grouped[byValue]);
					output.push({name: byValue, data: yValues, showInLegend: false});
				});
				return output;
			},
			/**
			 * Creates an array without duplicate values
			 * @param {array} array to be transformed
			 */
			getRidOfDuplicates: function(array) {
			   return Array.from(new Set(array));
			},
			/**
			 * Determines action that is to be carried on the given array and carries it out
			 * @param {array} array whose values are to be evaulated
			 */
			determineAction: function(array) {
				if (this.selectedOptions.func == 'none' || this.selectedOptions.func == 'max') {
					return this.maxOf(array);
				}
				else if (this.selectedOptions.func == 'sum') {
					return this.sumOf(array);
				}
				else if (this.selectedOptions.func == 'count') {
					return this.countOf(array);
				}
				else if (this.selectedOptions.func == 'mean') {
					return this.meanOf(array);
				}
				else if (this.selectedOptions.func == 'min') {
					return this.minOf(array);
				}
				else if (this.selectedOptions.func == 'median') {
					return this.medianOf(array);
				}
			},
			/**
			 * Calculates maximum of an array
			 * @param {array} array to calculate max of
			 */
			maxOf: function(array) {
				return array.reduce((max, val) => val > max ? val : max, array[0]);
			},
			/**
			 * Calculates sum of an array
			 * @param {array} array to calculate sum of
			 */
			sumOf: function(array) {
				return array.reduce((a, b) => a + b, 0);
			},
			/**
			 * Calculates mean of an array
			 * @param {array} array to calculate mean of
			 */
			meanOf: function(array) {
				var sum = 0;
				for (var i = 0; i < array.length; i++) {
				    sum += array[i];
				}
				return sum / array.length;
			},
			/**
			 * Calculates count of an array
			 * @param {array} array to calculate count of
			 */
			countOf: function(array) {
				return array.length;
			},
			/**
			 * Calculates median of an array
			 * @param {array} array to calculate median of
			 */
			medianOf: function(array) {
				array.sort(function(a, b) {
			      return a - b;
			    });
			    var mid = array.length / 2;
			    return mid % 1 ? array[mid - 0.5] : (array[mid - 1] + array[mid]) / 2;
			},
			/**
			 * Calculates minimum of an array
			 * @param {array} array to calculate minimum of
			 */
			minOf: function(array) {
				return array.reduce((min, val) => val < min ? val : min, array[0]);
			},
		}
	}
</script>