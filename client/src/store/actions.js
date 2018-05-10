import axios from 'axios'
import { tidyURL } from './helpers.js' 

export default {
	/**
	 * Fire mutation for success modal toggle
	 */
	setSuccessScreen: function({ commit }, payload) {
		commit('setSuccessScreen', payload);
	},
	/**
	 * Fire mutation for setting current repository name
	 */
	setCurrentRepoName: function({ commit }, payload) {
		commit('setCurrentRepoName', payload);
	},
	/**
	 * Fire mutation for setting current repository path
	 */
	setCurrentRepoPath: function({ commit }, payload) {
		commit('setCurrentRepoPath', payload);
	},
	/**
	 * Fire mutation for setting current branch and dispatch action to load commits
	 */
	setCurrentBranch: function({ commit, dispatch }, payload) {
		commit('setCurrentBranch', payload.branch);
		
		dispatch({
			type: 'loadCommits',
			path: payload.path,
			branch: payload.branch,
		});
	},
	/**
	 * Fire mutation for setting current repository branch
	 */
	resetCurrentBranch: function({ commit }) {
		commit('setCurrentBranch', 'master');
	},
	/**
	 * Fire mutation for setting current search path
	 */
	changeSearchPath: function({ commit }, payload) {
		commit('changeSearchPath', payload.path);
	},
	/**
	 * Retrieve compare profiles list from server and fire mutation
	 */
	getCompareProfilesList: function({ commit }, payload) {
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/profiles/' + payload.id + '/list';

		axios.get(URL).then(response => {
			if (response.status == 200) {
				commit('setCompareProfilesList', response.data);
			}
		})
		.catch(error => {
			commit('setError', error)
		});

	},
	/**
	 * Retrieve compare profiles' data from server and fire mutation
	 */
	getProfilesToCompare: function({ commit }, payload) {

		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/profiles/compare';

		axios.patch(URL, { baseline: payload.baseline, target: payload.target }).then(response => {
			if (response.status == 200) {
				commit('setProfilesToCompare', response.data);
			}
		})
		.catch(error => {
			commit('setError', error)
		});

	},
	/**
	 * Clears dashboard data 
	 */
	clearDashboard: function({ commit }) {
		commit('loadDashboard', { all: {time: 0, memory: 0, mixed: 0, all: 0}, branches: []});
	},
	/**
	 * Retrieve dashboard data from server and fire mutation
	 */
	loadDashboard: function({ commit }, payload) {

		var time = setTimeout(() => { 
			commit('setLoadingScreen', true); 
		}, 400);

		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/dashboard';

		axios.get(URL).then(response => {
			if (response.status == 200) {
				commit('loadDashboard', response.data);
				clearTimeout(time);
				commit('setLoadingScreen', false);
			}
		})
		.catch(error => {
			clearTimeout(time);
			commit('setLoadingScreen', false);
			commit('setError', error)
		});
	},
	/**
	 * Retrieve repositories data from server and fire mutation
	 */
	loadRepositories: function({ commit }, payload) { //OK
		
		var time = setTimeout(() => { 
			commit('setLoadingScreen', true); 
		}, 400);

		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/';

		axios.get(URL).then(response => {
			if (response.status == 200) {
				commit('loadRepositories', response.data);
				clearTimeout(time);
				commit('setLoadingScreen', false);
			}
		})
		.catch(error => {
			clearTimeout(time);
			commit('setLoadingScreen', false);
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to create a Perun instance over the repository
	 */
	integrateRepo: function({ commit }, payload) {

		const path = tidyURL(payload.path);
		var URL = '/repos/' + path + '/integrate';

		axios.patch(URL, payload).then(response => {
			if (response.status == 200) {
				
				commit({
					type: 'integrateRepo', 
					path: payload.path,
				});

				commit('setSuccessScreen', true);
				setTimeout(() => { commit('setSuccessScreen', false);}, 1000);
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false); }, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to remove a Perun instance over the repository
	 */
	removeRepoIntegration: function({ commit }, payload) {
		
		const path = tidyURL(payload.path);
		var URL = '/repos/' + path + '/remove';

		axios.patch(URL).then(response => {
			if (response.status == 200) {
				commit({
					type: 'removeRepoIntegration', 
					path: payload.path,
				});
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Retrieve branches list from the server and fire mutation
	 */
	loadBranches: function({ commit }, payload) {

		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/branches';

		axios.get(URL).then(response => {
			if (response.status == 200) {
				commit('setOptionalBranches', response.data);	
			}
		})
		.catch(error => {
			commit('setError', error)
		});

	},
	/**
	 * Retrieve commits' data from the server and fire mutation
	 */
	loadCommits: function({ commit }, payload) {
		
		var time = setTimeout(() => { 
			commit('setLoadingScreen', true);
		}, 400);
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/' + payload.branch + '/commits';
		
		axios.get(URL).then(response => {
			if (response.status == 200) {
				commit('loadCommits', response.data);	
			}
			clearTimeout(time);
			commit('setLoadingScreen', false);
		})
		.catch(error => {
			clearTimeout(time);
			commit('setLoadingScreen', false);
			commit('setError', error)
		});
	},
	/**
	 * Retrieve commit info from the server and fire mutation
	 */
	loadCommitInfo: function({ commit }, payload) {
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/commits/' + payload.commitId + '/info';

		axios.get(URL).then(response => {
			if (response.status == 200) {
				commit('loadCommitInfo', response.data);
			}
		})
		.catch(error => {
			commit('setError', error)
		});
	},
	/**
	 * Retrieve all repository profiles' data from the server and fire mutation
	 */
	loadRepoProfiles: function({ commit }, payload) {
		
		var time = setTimeout(() => { 
			commit('setLoadingScreen', true);
		}, 400);

		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/profiles';
		
		axios.get(URL).then(response => {
			commit('loadRepoProfiles', response.data);
			clearTimeout(time);
			commit('setLoadingScreen', false);
		})
		.catch(error => {
			clearTimeout(time);
			commit('setLoadingScreen', false);
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Retrieve all commit profiles' data from the server and fire mutation
	 */
	loadCommitProfiles: function({ commit }, payload) { //OK
		
		var time = setTimeout(() => { 
			commit('setLoadingScreen', true);
		}, 400);

		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/commits/' + payload.commitId + '/profiles';
		
		axios.get(URL).then(response => {
			commit('loadCommitProfiles', response.data);
			clearTimeout(time);
			commit('setLoadingScreen', false);
		})
		.catch(error => {
			clearTimeout(time);
			commit('setLoadingScreen', false);
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Retrieve all profiles data from the server and fire mutation
	 */
	loadProfile: function({ commit }, payload) { //OK

		var time = setTimeout(() => { 
			commit('setLoadingScreen', true);
		}, 400);

		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/' + payload.commitId + '/profiles/' + payload.profileId + '/info';

		axios.get(URL).then(response => {
			commit('loadProfile', response.data);
			clearTimeout(time);
			commit('setLoadingScreen', false);
		})
		.catch(error => {
			clearTimeout(time);
			commit('setLoadingScreen', false);
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to register the profile and fire mutation
	 */
	registerProfile: function({ commit }, payload) { //OK
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/' + payload.commitId + '/profile-register';
		
		axios.patch(URL, { path: payload.profilePath, id: payload.profileId }).then(response => {
			if (response.status == 200) {
			
				commit({
					type: 'registerProfile',
					profilePath: response.data.path,
					profileId: payload.profileId,
				});

				commit('setSuccessScreen', true);
				setTimeout(() => { commit('setSuccessScreen', false);}, 1000);
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to unregister the profile and fire mutation
	 */
	unregisterProfile: function({ commit }, payload) { //OK
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/' + payload.commitId + '/profile-unregister';

		axios.patch(URL, { id: payload.profileId }).then(response => {
			if (response.status == 200) {
				commit({
					type: 'unregisterProfile',
					profileId: payload.profileId,
				});
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Retrieve global settings data from server and fire mutation
	 */
	loadGlobalSettings: function({ commit }) {
		var URL = '/global-settings';
		axios.get(URL).then(response => {
			commit('loadGlobalSettings', response.data);
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to save global settings
	 */
	saveGlobalSettings: function({ commit }, payload) {
		
		var URL = '/global-settings/save';
		
		axios.patch(URL, payload).then(response => {
			if (response.status == 200) {
				commit('setSuccessScreen', true);
				var time = setTimeout(() => { commit('setSuccessScreen', false);}, 1000);
				commit('saveGlobalSettings', payload);
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Retrieve local settings data from server and fire mutation
	 */
	loadLocalSettings: function({ commit }, payload) {
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/local-settings';

		axios.get(URL).then(response => {
			commit('loadLocalSettings', response.data);
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to save local settings
	 */
	saveLocalSettings: function({ commit }, payload) {
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/local-settings/save';
		
		axios.patch(URL, payload).then(response => {
			if (response.status == 200) {
				
				commit('setSuccessScreen', true);
				setTimeout(() => { commit('setSuccessScreen', false);}, 1000);

				commit('saveLocalSettings', payload);
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to save job matrix settings
	 */
	saveJobMatrixSettings: function({ commit }, payload) {
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/local-settings/job-matrix/save';
		
		axios.patch(URL, payload).then(response => {
			if (response.status == 200) {

				commit('setSuccessScreen', true);
				setTimeout(() => { commit('setSuccessScreen', false);}, 1000);

				commit('saveJobMatrixSettings', payload);
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to collect new profiles based on ad hoc specification
	 * (for future development)
	 */
	collectNewProfile: function({ commit }, payload) {
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/' + payload.commitId + '/single-job/collect-new';
		
		axios.get(URL, payload).then(response => {
			commit('loadCommitProfiles', response.data);
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to collect new profiles based on pre-defined specification
	 */
	collectNewProfileJobMatrix: function({ commit }, payload) {
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/' + payload.commitId + '/' + 'job-matrix/collect-new';

		axios.get(URL, payload).then(response => {
			if (response.status == 200) {

				commit('setSuccessScreen', true);
				setTimeout(() => { commit('setSuccessScreen', false);}, 1000);

				commit('loadCommitProfiles', response.data);
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	},
	/**
	 * Send request to postprocess the profile
	 */
	postprocessProfile: function({ commit }, payload) {
		
		payload.path = tidyURL(payload.path);
		var URL = '/repos/' + payload.path + '/profiles/' + payload.profilePath + '/postprocess';

		axios.patch(URL, { registration: payload.registration, specification: payload.specification }).then(response => {
			if (response.status == 200) {
				commit('setSuccessScreen', true);
				setTimeout(() => { commit('setSuccessScreen', false);}, 1000);
			}
		})
		.catch(error => {
			commit('setErrorScreen', true);
			setTimeout(() => { commit('setErrorScreen', false);}, 1000);
			commit('setError', error)
		});
	}
}