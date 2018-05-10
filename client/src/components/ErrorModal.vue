<template>
	<transition name="custom-modal-fade">
		<div class="custom-modal-backdrop error-modal">
			<div class="custom-modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
				
				<div class="custom-modal-header" id="modalTitle">
				</div>
				
				<div class="custom-modal-body" id="modalDescription">
					<div class="custom-message-modal-icon error">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
					</div>
					<div><slot name="header"></slot></div>
				</div>
			</div>
		</div>
	</transition>
</template>

<style scoped>
	.error-modal .custom-modal {
		background-color: #37474F;
		overflow: hidden;
		width: 40%;
		height: 280px;
		border-radius: 3px;
		margin-bottom: -10px;
		box-shadow: 0 5px 15px rgba(0,0,0,0.3);
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.error-modal .custom-modal-header {
		color: white;
		background-color: white;
		height: 40px;
	}

	.error-modal .custom-modal-header svg {
		fill: #455A64;
		padding: 8px;
		height: 40px;
		width: 40px;
		border-radius: 100%;
	}

	.error-modal .custom-modal-header svg:hover {
		background-color: #78909C;
		fill: white;
	}

	.error-modal .custom-modal-body {
		position: relative;
		padding: 10px 30px 30px 30px;
		background-color: white;
		overflow: hidden;
		flex: 0 1 90%;
		text-align: center;
		color: #455A64;
		font-weight: 200;
	}

	.custom-message-modal-icon.error svg {
		fill: #EF5350;
	}
</style>