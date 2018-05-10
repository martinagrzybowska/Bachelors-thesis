<template>
	<span>{{ displayNumber }}</span>
</template>

<script type="text/javascript">
	export default {
		props: {
			number: {
				type: Number,
				required: true,
				default: 0,
			},
		},
		data: function() {
			return {
				displayNumber: 0,
				interval: false,
			}
		},
		mounted: function() {
			clearInterval(this.interval);
			if (this.number == this.displayNumber) {
				return;
			}

			this.interval = window.setInterval(function() {
				if (this.displayNumber != this.number) {
					var difference = (this.number - this.displayNumber) / 10;
					difference = difference >= 0 ? Math.ceil(difference) : Math.floor(difference);
					this.displayNumber = this.displayNumber + difference;
				}
			}.bind(this), 30);
		},
	}

</script>