<template>
	<transition name="custom-modal-fade">
		<div class="custom-modal-backdrop success-modal">
			<div class="custom-modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
				
				<div class="custom-modal-header" id="modalTitle"></div>
				
				<div class="custom-modal-body" id="modalDescription">
					<div class="custom-message-modal-icon success">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z"/></svg>
					</div>
					<div><slot name="header"></slot></div>
				</div>
			</div>
		</div>
	</transition>
</template>

<style scoped>
	.success-modal .custom-modal {
		background-color: white;
		width: 40%;
		height: 280px;
		border-radius: 3px;
		margin-bottom: -10px;
		box-shadow: 0 5px 15px rgba(0,0,0,0.3);
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	.success-modal .custom-modal-header,
	.custom-modal-footer {
		background-color: white;
	}

	.success-modal .custom-modal-body {
		position: relative;
		padding: 10px 30px 30px 30px;
		background-color: white;
		overflow: hidden;
		flex: 0 1 90%;
		text-align: center;
		color: #455A64;
		font-weight: 200;
	}
</style>