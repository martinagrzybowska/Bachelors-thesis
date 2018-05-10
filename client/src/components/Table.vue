<!-- <template>
	<div>
		<div class="search-bar-container">
			 <input type="text" class="search-bar" v-model="filterKey" placeholder="Search repositories">
		</div>

		<table class="table-container table">
			<thead class="table-header">
				<tr>
					<th class="table-header-item" v-for="column in tableColumnNames">
						<div v-if="column.type == 'blank'">
							<span>{{ column.name }}</span>
							<span class="arrow dsc"></span>
						</div>
						<div v-else-if="column.type == 'button'">
							<span></span>
						</div>
					</th>
				</tr>
			</thead>
			<tbody class="table-body">
				<tr class="table-body-row" v-for="tableRow in tableRows">
					<td class="table-body-row-item" v-for="tableCell in tableRow">
						<template v-if="determineButton(index)">	
							<div class="table-button">
							<span>ha</span>
						</template>
					</td>
					
				</tr>
			</tbody>
		</table>
		<div class="table-pagination">
			<div class="page-range">
				<span>Display per page: </span>
				<div class="range-number">
					<span>5</span>
					<span>10</span>
					<span>20</span>
					<span>50</span>
				</div>
			</div>
			<div class="page-numbering">
				<div><span class="arrow hollow left"></span><span>PREVIOUS</span></div>
				<div class="page-number-container">
					<span class="page-number no-pointer">1</span>
					<span class="no-pointer"> of </span>
					<span class="page-number">2</span>
				</div>
				<div ><span>NEXT</span><span class="arrow hollow right"></span></div>
			</div>
		</div>
	</div>
</template>


<script type="text/javascript">
	export default {
		props: [
			'tableColumnNames',
			'buttonIndices',
			'iconIndices',
		],
		data: function() {
			return {

			}
		}
		computed: {

		},
	}
</script>

<style scoped>
	
	.search-bar-container {
		text-align: right;
		margin-bottom: 0!important;
	}

	.search-bar {
		border: 1px solid #dbe6ec;
		border-radius: 2px;
		color: #768389;
		padding: 4px 12px;
		height: 28px;
		width: 300px;
		font-size: 13px;
		box-shadow: inset 0 1px 1px rgba(0,0,0,.075);
	}

	.search-bar::placeholder {
		color: #768389;
	}

	.table-header, .table-body-row {
		width: 100%;
	}

	.table-container {
		border-bottom: 2px solid #dbe6ec!important;
		margin-bottom: 0!important;
	}

	.table-header th {
		border-top: none!important;
		border-bottom: 2px solid #dbe6ec!important;
	}

	.table-body-row:not(:last-child) {
		border-bottom: 1px solid #dbe6ec!important;
	}

	.table-body-row:not(:last-child) {
		border-bottom: 1px solid #dbe6ec!important;
	}

	.table-body-row:nth-child(odd) {
		background-color: #f4f9f9!important;
	}

	.table-body-row td {
		padding: 0 .80rem!important;
	}

	.table-header-item:not(:last-child) div {
		width: 100%;
		height: 20px;
		vertical-align: center;
		border-right: 1px solid #dbe6ec;
	}

	.table-body-row-item>span {
		overflow: hidden;
    	text-overflow: ellipsis;
    	white-space: nowrap;
    	word-wrap: normal;
    	color: #585c5e;
   		font-weight: 400;
    	line-height: 48px;
    	display: inline-block;
    	font-size: 13px;
    	vertical-align: top;
	}

	.table-header .table-header-item {
    	align-items: center;
    	text-transform: uppercase;
	}
	
	.table-header .table-header-item span {
		color: #768389;
    	font-size: 12px;
    	font-weight: 400;
	}
</style> -->