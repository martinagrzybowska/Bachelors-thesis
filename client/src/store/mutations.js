export default {
	
	setError: function(state, payload) {
		state.error = payload;
	},

	setLoadingScreen: function(state, payload) {
		state.loadingScreen = payload;
	},

	setSuccessScreen: function(state, payload) {
		state.successScreen = payload;
	},

	setErrorScreen: function(state, payload) {
		state.errorScreen = payload;
	},

	setCurrentRepoName: function(state, payload) {
		state.currentRepoName = payload;
	},

	setCurrentRepoPath: function(state, payload) {
		state.currentRepoPath = payload;
	},

	setCurrentBranch: function(state, payload) {
		state.currentBranch = payload;
	},

	setOptionalBranches: function(state, payload) {
		state.optionalBranches = payload.optionalBranches;
	},

	changeSearchPath: function(state, payload) {
		state.searchPath = payload;
	},

	loadDashboard: function(state, payload) {
		state.dashboard.all = payload.all;
		state.dashboard.branches = payload.branches;
	},

	loadRepositories: function(state, payload) {
		state.repositories = payload.repositories;
	},

	setCompareProfilesList: function(state, payload) {
		state.compareProfilesList = payload.profiles;
	},

	setProfilesToCompare: function(state, payload) {
		state.compareProfiles.baseline = payload.profiles.baseline;
		state.compareProfiles.target = payload.profiles.target;
	},

	integrateRepo: function(state, payload) {
		var repo = state.repositories.find(repo => {
			return repo.path == payload.path;
		});
		repo.integration = 'integrated';
	},

	removeRepoIntegration: function(state, payload) {
		var repo = state.repositories.find(repo => {
			return repo.path == payload.path;
		});
		repo.integration = 'missing';
	},

	loadCommits: function(state, payload) {
		state.commits = payload.commits;
	},

	loadCommitInfo: function(state, payload) {
		state.commitInfo.author = payload.commit.author;
		state.commitInfo.message = payload.commit.message;
		state.commitInfo.date = payload.commit.date;
		state.commitInfo.parents = payload.commit.parents;
	},

	loadProfile: function(state, payload) {
		state.profile = payload.profile;
	},

	loadRepoProfiles: function(state, payload) {
		state.profiles = payload.profiles;
	},

	loadCommitProfiles: function(state, payload) {
		state.profiles = payload.profiles;
	},

	registerProfile: function(state, payload) {
		var profile = state.profiles.find(profile => {
			return profile.id == payload.profileId;
		});
		profile.registered = true;
		state.profile.registered = true;
		profile.action = 'remove';
		profile.path = payload.profilePath;
	},

	unregisterProfile: function(state, payload) {
		var index = state.profiles.findIndex(profile => {
			return profile.id == payload.profileId;
		});
		state.profiles.splice(index, 1);
	},

	addNewProfile: function(state, payload) {
		payload.profiles.forEach(profile => {
			state.profiles.push(profile);
		});
	},

	postprocessProfile: function(state, payload) {
		var postprocessors = state.profile.collection_configuration.find(item => {
			return (item.postprocessors != undefined);
		});
		postprocessors.postprocessors.push(payload.postprocessor);
	},
	
	loadGlobalSettings: function(state, payload) {
		state.globalSettings.general = payload.globalSettings.general;
		state.globalSettings.format = payload.globalSettings.format;
	},

	saveGlobalSettings: function(state, payload) {
		var row  = state.globalSettings[payload.section].find(row => {
			return row.name == payload.name;
		});
		row.value = payload.value;
	},

	loadLocalSettings: function(state, payload) {
		state.localSettings = payload.localSettings;
	},

	saveLocalSettings: function(state, payload) {
		var row  = state.localSettings[payload.section].find(row => {
			return row.name == payload.name;
		});
		row[payload.item] = payload.value;
	},

	saveJobMatrixSettings: function(state, payload) {
		state.localSettings.jobMatrix[payload.section][payload.name] = payload.value.slice(0);
	},

}