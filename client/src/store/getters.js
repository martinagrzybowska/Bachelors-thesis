export default {
	loadingScreen: function(state) {
		return state.loadingScreen;
	},
	successScreen: function(state) {
		return state.successScreen;
	},
	errorScreen: function(state) {
		return state.errorScreen;
	},
	compareProfilesList: function(state) {
		return state.compareProfilesList;
	},
	compareProfiles: function(state) {
		return state.compareProfiles;
	},
	dashboard: function(state) {
		return state.dashboard;
	},
	currentRepoName: function(state) {
		return state.currentRepoName;
	},
	currentRepoPath: function(state) {
		return state.currentRepoPath;
	},
	currentBranch: function(state) {
		return state.currentBranch;
	},
	optionalBranches: function(state) {
		return state.optionalBranches;
	},
	searchPath: function(state) {
		return state.searchPath;
	},
	repositories: function(state) {
		return state.repositories;
	},
	commits: function(state) {
		return state.commits;
	},
	commitInfo: function(state) {
		return state.commitInfo;
	},
	profiles: function(state) {
		return state.profiles;
	},
	profile: function(state) {
		return state.profile;
	},
	registeredProfiles: function(state) {
		return state.profiles.filter(profile => {
			return profile.registered;
		});
	},
	pendingProfiles: function(state) {
		return state.profiles.filter(profile => {
			return !profile.registered;
		});
	},
	globalSettings: function(state) {
		return JSON.parse(JSON.stringify(state.globalSettings));
	},
	localSettings: function(state) {
		return JSON.parse(JSON.stringify(state.localSettings));
	},
	revertLocalSettings: function(state) {
		return JSON.parse(JSON.stringify(state.localSettings));
	}
}