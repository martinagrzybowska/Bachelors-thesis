<template>
	<transition name="custom-modal-fade">
		<div class="custom-modal-backdrop remove-modal" @click.self="close()">
			<div class="custom-modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
				
				<div class="custom-modal-header" id="modalTitle">
					<svg @click="close" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M323.1 441l53.9-53.9c9.4-9.4 9.4-24.5 0-33.9L279.8 256l97.2-97.2c9.4-9.4 9.4-24.5 0-33.9L323.1 71c-9.4-9.4-24.5-9.4-33.9 0L192 168.2 94.8 71c-9.4-9.4-24.5-9.4-33.9 0L7 124.9c-9.4 9.4-9.4 24.5 0 33.9l97.2 97.2L7 353.2c-9.4 9.4-9.4 24.5 0 33.9L60.9 441c9.4 9.4 24.5 9.4 33.9 0l97.2-97.2 97.2 97.2c9.3 9.3 24.5 9.3 33.9 0z"/></svg>
				</div>
				
				<div class="custom-modal-body" id="modalDescription">
					<div class="custom-message-modal-icon remove">
						<svg @click="close" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M504 256c0 136.997-111.043 248-248 248S8 392.997 8 256C8 119.083 119.043 8 256 8s248 111.083 248 248zm-248 50c-25.405 0-46 20.595-46 46s20.595 46 46 46 46-20.595 46-46-20.595-46-46-46zm-43.673-165.346l7.418 136c.347 6.364 5.609 11.346 11.982 11.346h48.546c6.373 0 11.635-4.982 11.982-11.346l7.418-136c.375-6.874-5.098-12.654-11.982-12.654h-63.383c-6.884 0-12.356 5.78-11.981 12.654z"/></svg>
					</div>
					<div><slot name="header"></slot></div>
				</div>

					
				<div class="custom-modal-footer">
					<div class="table-button" @click="confirm()">
						<span>proceed</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119.033 8 8 119.033 8 256s111.033 248 248 248 248-111.033 248-248S392.967 8 256 8zm0 48c110.532 0 200 89.451 200 200 0 110.532-89.451 200-200 200-110.532 0-200-89.451-200-200 0-110.532 89.451-200 200-200m140.204 130.267l-22.536-22.718c-4.667-4.705-12.265-4.736-16.97-.068L215.346 303.697l-59.792-60.277c-4.667-4.705-12.265-4.736-16.97-.069l-22.719 22.536c-4.705 4.667-4.736 12.265-.068 16.971l90.781 91.516c4.667 4.705 12.265 4.736 16.97.068l172.589-171.204c4.704-4.668 4.734-12.266.067-16.971z"/></svg>
					</div>
					<div class="table-button remove" @click="close()">
						<span>cancel</span>
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm101.8-262.2L295.6 256l62.2 62.2c4.7 4.7 4.7 12.3 0 17l-22.6 22.6c-4.7 4.7-12.3 4.7-17 0L256 295.6l-62.2 62.2c-4.7 4.7-12.3 4.7-17 0l-22.6-22.6c-4.7-4.7-4.7-12.3 0-17l62.2-62.2-62.2-62.2c-4.7-4.7-4.7-12.3 0-17l22.6-22.6c4.7-4.7 12.3-4.7 17 0l62.2 62.2 62.2-62.2c4.7-4.7 12.3-4.7 17 0l22.6 22.6c4.7 4.7 4.7 12.3 0 17z"/></svg>
					</div>
				</div>
			</div>
		</div>
	</transition>
</template>

<script type="text/javascript">
	export default {
		methods: {
			/**
			 * Close event
			 * @event close
			 */
			close: function() {
				this.$emit('close');
			},
			/**
			 * Confirm event
			 * @event confirm
			 */
			confirm: function() {
				this.$emit('confirm');
			},
		},
	};
</script>

<style scoped>
	.custom-modal {
		width: 40%;
		height: 330px;
	}

	.custom-modal-header,
	.custom-modal-footer {
		flex: 0 0 60px;
	}

	.remove-modal .custom-modal-header svg {
		fill: #455A64;
		padding: 8px;
		height: 40px;
		width: 40px;
		border-radius: 100%;
	}

	.remove-modal .custom-modal-header svg:hover {
		background-color: #78909C;
		fill: white;
	}

	.custom-modal-header {
		background-color: white;
		justify-content: flex-end;
		padding-top: 20px;
		padding-bottom: 20px;
		flex: 0 0 70px;
	}

	.remove-modal .custom-modal-footer {
		padding-bottom: 20px;
		height: 75px;
		justify-content: center;
		background-color: white;
		flex: 0 0 80px;
	}
	.remove-modal .custom-modal-body {
		position: relative;
		padding: 0 60px 20px 60px;
		background-color: white;
		overflow: hidden;
		flex: 0 1 80%;
		text-align: center;
		color: #455A64;
		font-weight: 200;
	}
	.remove-modal .custom-modal-footer .table-button {
		height: 35px;
		width: 110px;
	}
	.remove-modal .custom-modal-footer .table-button svg {
		height: 35px;
	}
</style>