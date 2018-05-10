<template>
	<transition name="custom-modal-fade">
		<div class="custom-modal-backdrop loading-modal">
			<div class="loading-wrapper">
				<loader color="white" height="100px" width="200px" size="30px"></loader>
			</div>
		</div>
	</transition>
</template>

<style scoped>
	.loading-modal {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	.loading-wrapper {
		flex: 0 0 60px;
		width: 300px;
	}
	.v-spinner {
		margin: auto;
	}

</style>