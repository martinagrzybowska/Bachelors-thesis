import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters.js'
import actions from './actions.js'
import mutations from './mutations.js'

Vue.use(Vuex);
import createPersistedState from 'vuex-persistedstate'

export const store = new Vuex.Store({
	plugins: [
		createPersistedState({
			reducer: state => ({
				currentRepoName: state.currentRepoName,
				currentRepoPath: state.currentRepoPath,
				currentBranch: state.currentBranch,
				searchPath: state.searchPath,
			}),
		}),
	],
	state: {
		loadingScreen: false,
		successScreen: false,
		errorScreen: false,
		currentRepoName: '',
		currentRepoPath: '',
		currentBranch: 'master',
		optionalBranches: [
			'master',
			'bug1Fix',
			'bug2Fix',
		],
		error: '',
		dashboard: {all: {time: 0, memory: 0, mixed: 0, all: 900}, branches: []},
		searchPath: '',
		repositories: [],
		profiles: [],
		commits: [],
		commitInfo: {
			'author': '',
			'date': '',
			'message': '',
			'parents': [],
		},
		profile: {
			profiled_command: [
				{ 'time of collection' : '' },
				{ 'profile type' : '' },
				{ 'command' : '' },
				{ 'arguments' : '' },
				{ 'workload' : '' },
				{ 'units' : '' },
				{ 'path' : '' },
			],
			collection_configuration: [
				{ 'collector' : '' },
				{ 'postprocessors' : [] },
			],
			chart_options: [],
			chart_numerical_options: [],
			resources: {},
		},
		compareProfilesList: [],
		compareProfiles: {
			'baseline': {
				chart_options: [],
				chart_numerical_options: [],
			},
			'target': {
				chart_options: [],
				chart_numerical_options: [],
			}
		},
		globalSettings: {
			general: [],
			format: [],
		},
		localSettings: {
			general: [],
			format: [],
			vcs: [],
			jobMatrix: {
				profiledCommands: {
					commands: [],
					arguments: [],
					workload: [],
				},
				collectionSpecification: {
					collectors: [],
					postprocessors: [],
				},
			},
		},
	},
	getters: getters,
	mutations: mutations,
	actions: actions,
});

