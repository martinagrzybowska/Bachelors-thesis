<!-- 
repo_local: [
	master: [
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: ['bugfix1'] },
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },

	]
	bugfix1: [
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
		{ commit: '04akka', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
		{ commit: '04akka', profiles: [], mergeInto: 'master', mergeFrom: '', branches: [] },
	]
],

existingBranches: {},

recurse: function(s_branch, branchObject, branchName, flag) {
	s_branch.forEach(s_commmit => {
		
		if (jsonCommit.mergeInto == '' && jsonCommit.mergeFrom == '') { //pokial je to len obyc commit
			
			branchObject.commit(s_commmit.commit); // commitni
			jsonCommit.branches.forEach(childBranchName => { // pozri sa na branche, ake z neho vychadzaju
				if (existingBranches.childBranchName == undefined) { // pokial tam nejaka je a este nie je definovana
					var tmp = existingBranches[s_branch].branch(childBranchName); // vytvor ju pod jej menom
					existingBranches[childBranchName] = tmp; // a potlac ju do objektu pod klucom jej mena 
				}
			});
		}
		else {
			if (jsonCommit.mergeFrom != '') {
				if (repo_local[jsonCommit.mergeFrom][0].mergeInto == branchName) { //ak v repo v branchi prvy commit mergeInto je meno akt branche
					branchObject.merge(existingBranches[jsonCommit.mergeFrom]); // vytvor commit
					repo_local[jsonCommit.mergeFrom].slice(0, 1); // zmaz ho z detskej branche
				}
				else {
					recurse(repo_local[jsonCommit.mergeFrom], existingBranches[jsonCommit.mergeFrom], jsonCommit.mergeFrom, true);
				}
			}
			
			if (jsonCommit.mergeInto != '') {
				if (repo_local[jsonCommit.mergeFrom][0].mergeFrom == branchName) { //ak v repo v branchi prvy commit mergeInto je meno akt branche
					branchObject.merge(existingBranches[jsonCommit.mergeInto]); // vytvor commit
					repo_local[jsonCommit.mergeInto].slice(0, 1); // zmaz ho z detskej branche
				}
				else {
					recurse(repo_local[jsonCommit.mergeInto], existingBranches[jsonCommit.mergeInto], jsonCommit.mergeInto, true);
				}
			}
		}

		repo_local[branchName].slice(repo_local[branchName].indexOf(s_commmit), 1); // zmaz ten commit zo zoznamu, je vybaveny
		
		if (flag) {
			return;
		}

	});
} -->
<!-- createNewBranch: function(jsonCommit, branchName) {
			// 	for (var x = 0; x < jsonCommit.branches.length; x++) {
			// 		var childBranchName = jsonCommit.branches[x];
					
			// 		// if there is no such branch yet, it is created and stored
			// 		if (this.existingBranches.childBranchName == undefined) { 
			// 			var tmp = this.existingBranches[branchName].branch(childBranchName);
			// 			this.existingBranches[childBranchName] = tmp;
			// 		}
			// 	}
			// },
			// recurse: function(branchJson, branchObject, branchName, parentBranch, origin) {
				
			// 	for (var i = 0; i < branchJson.length; i++) {				
			// 		var jsonCommit = branchJson[i];

			// 		if (jsonCommit.level != undefined) {
			// 			return;
			// 		}

			// 		if (jsonCommit.mergeInto == '' && jsonCommit.mergeFrom == '') {
			// 			// commit
			// 			branchObject.commit(jsonCommit.commit);
			// 			// if there are any children branches, create them
			// 			this.createNewBranch(jsonCommit, branchName);
			// 			// since the commit is now finished, remove it from the list
			// 			this.repoHistory[branchName].splice(0, 1);
			// 		}
			// 		else {
			// 			if (jsonCommit.mergeFrom != '') {

			// 				// if the values of mergeFrom (of current branch) and mergeInto (of the branch which is supposed to be merged
			// 				// are equal, merge the branches)
			// 				if (this.repoHistory[jsonCommit.mergeFrom][0].mergeInto == branchName) {
			// 					if (origin == 'into') {
			// 						this.existingBranches[jsonCommit.mergeFrom].merge(branchObject);
			// 					}
			// 					else {
			// 						branchObject.merge(this.existingBranches[jsonCommit.mergeFrom]);
			// 					}
			// 					// if there are any children branches, create them
			// 					this.createNewBranch(jsonCommit, branchName);
			// 					// delete the commit from the merged branch
			// 					this.repoHistory[jsonCommit.mergeFrom].splice(0, 1);
			// 					// recurse termination condition
			// 					if (jsonCommit.mergeFrom == parentBranch) {
			// 						// delete the merged commit from the current branch
			// 						this.repoHistory[branchName].splice(0, 1);
			// 						return;
			// 					}
			// 				}
			// 				else {
			// 					var copy = JSON.parse(JSON.stringify(this.repoHistory[jsonCommit.mergeFrom]));
			// 					this.recurse(copy, this.existingBranches[jsonCommit.mergeFrom], jsonCommit.mergeFrom, branchName, 'from');
						
			// 					// recurse termination condition
			// 					if (jsonCommit.mergeFrom == parentBranch) {
			// 						return;
			// 					}
			// 				}
			// 			}
						
			// 			if (jsonCommit.mergeInto != '') {
			// 				if (this.repoHistory[jsonCommit.mergeInto][0].mergeFrom == branchName) { 
			// 					if (origin == 'from') {
			// 						branchObject.merge(this.existingBranches[jsonCommit.mergeInto]);
			// 					}
			// 					else {
			// 						this.existingBranches[jsonCommit.mergeInto].merge(branchObject);
			// 					}
																
			// 					// if there are any children branches, create them
			// 					this.createNewBranch(jsonCommit, branchName);

			// 					this.repoHistory[jsonCommit.mergeInto].splice(0, 1);

			// 					if (jsonCommit.mergeInto == parentBranch) {
			// 						this.repoHistory[branchName].splice(0, 1);
			// 						return;
			// 					}
			// 				}
			// 				else {
			// 					var copy = JSON.parse(JSON.stringify(this.repoHistory[jsonCommit.mergeInto]));
			// 					this.recurse(copy, this.existingBranches[jsonCommit.mergeInto], jsonCommit.mergeInto, branchName, 'into');
								
			// 					if (jsonCommit.mergeInto == parentBranch) {
			// 						return;
			// 					}
			// 				}
			// 			}
			// 		}
			// 	}
			// },
			// fill: function() {
			// 	from_server = {
			// 		master: [
			// 			{ commit: 'm1', parents: [], initial: true}
			// 			{ commit: 'm2', parents: ['m1'], initial: false}
			// 			{ commit: 'm3', parents: [], initial: false}
			// 		],
			// 		bugfix1: [
			// 			{ commit: 'bf11', parents: ['m2'], initial: true}
			// 			{ commit: 'bf12', parents: ['bf11'], initial: false}
			// 			{ commit: 'bf13', parents: ['bf12','m3'], initial: false}
			// 		]
			// 	}
				
			// 	output = {};

			// 	branches.forEach((branch) => {
			// 		output[branch] = [];
			// 	});

			// 	commits.forEach((commit) => {
			// 		var item = { commit: commit.commit, profiles: [], mergeInto: '', mergeFrom: '', branches: [] };
			// 		if (commit.initial) {
			// 			for (var iter = 0; iter < commits.length; iter++) {
			// 				if (commit.parents[0] == commits[iter].commit) {
			// 					item.branches.push(commits[iter].branch);
			// 				}
			// 			}
			// 		}


			// 		output[commit.branch].unshift(item);
			// 	});


				
			// 	Object.keys(from_server).forEach((branch) => {
			// 		output[branch] = [];
				
			// 		for (var iter = 0; iter < from_server[branch].length; iter++) {
			// 			output[branch].append({commit: from_server[branch][iter].commit, profiles: [], mergeInto: '', mergeFrom: '', branches: []})

			// 			if (from_server[branch][iter].parents.length == 2) {
			// 				if (from_server[branch][iter].parents[0] != from_server[branch][iter - 1].commit) {
			// 					var commit = from_server[branch][iter].parents[0];
			// 				}
			// 				else {
			// 					var commit = from_server[branch][iter].parents[1];
			// 				}

			// 				Object.keys(from_server).forEach((parent_branch) => {
			// 					if (parent_branch != branch) {
			// 						for (var iter = 0; iter < from_server[parent_branch].length; iter++) {
			// 							if (from_server[parent_branch].commit == commit) {
			// 								from_server[parent_branch].merge_into = branch;

			// 							}
			// 						}
			// 					}
			// 				}
			// 			}

			// 		}

			// 		if (branch != 'master') {
			// 			Object.keys(from_server).forEach((parent_branch) => {
			// 				if (parent_branch != branch) {
			// 					for (var iter = 0; iter < from_server[parent_branch].length; iter++) {
			// 						if (from_server[parent_branch].commit == from_server[branch][0].parents[0]) {
			// 							from_server[parent_branch].branches.append(branch);
			// 						}
			// 					}
			// 				}
			// 			}
			// 		}



			// 	});
			// },
			// bla: function() {
			// 	const myTemplate = new GitGraph.Template(this.myTemplateConfig);

			// 	this.gitgraph = new GitGraph({
			// 		  template: myTemplate,
			// 		  orientation: "vertical",
			// 		  mode: "expand",
			// 	});

			// 	const master = this.gitgraph.branch("master");
			// 	this.existingBranches['master'] = master;

			// 	// this.createAllBranches();
			// 	const copy = JSON.parse(JSON.stringify(this.repoHistory.master));
			// 	this.recurse(copy, master, 'master', '', '');

			// 	Object.keys(this.repoHistory).forEach(branchName => {
			// 		if (this.repoHistory[branchName].length > 0) {
			// 			if (this.existingBranches[branchName] != undefined) {
			// 				var branchJson = JSON.parse(JSON.stringify(this.repoHistory[branchName]));
			// 				this.recurse(branchJson, this.existingBranches[branchName], branchName, '', '');
			// 			}
			// 		}
			// 	});

				// console.log(this.repoHistory);
				// console.log(this.existingBranches);

				// var highestLevel = 0;
				// Object.keys(this.repoHistory).forEach(branchName => {
				// 	var tmp = this.repoHistory[branchName][this.repoHistory[branchName].length - 1].level;
				// 	if (tmp > highestLevel) {
				// 		highestLevel = tmp;
				// 	}
				// });
				// console.log("navyssi level je " + highestLevel);

				// this.repoHistory.master.forEach((masterCommit, index) => {
				// 	master.commit('tu som');
				// 	this.recurse(this.repoHistory.master[index], master);
				// });

				// var pokus = master.branch('pokus');
				// pokus.commit('bla');
				// var pokus2 = master.branch('pokus2');
				// pokus2.commit('bla1');
				// pokus.merge(master);
				// pokus2.merge(master);
				// pokus2.commit('ahoj');
				// master.merge(pokus2);
				// master.commit('aa');
				// master.commit({});
				// // master.merge(pokus);
				// // pokus.commit('bla');
				// // pokus.merge(master);
				// // pokus.merge(master);

				// console.log(this.gitGraphBranches);
			// },
		// 	draw: function() {
		// 		var ctx = document.getElementById('gitGraph').getContext('2d');
		// 		ctx.scale(2, 3);
		// 	}
		// },
		// mounted: function() {
		// 	this.bla();
		// 	this.draw(); -->


<!-- // repoHistory: {
				// 	master: [
				// 		{	commit: '0aaaa', profiles: [], merge: [], branches: {}	},
				// 		{	commit: '0xaf65a', profiles: [], merge: [],
				// 				branches: {
				// 					'bigfix1' : [
				// 						{	commit: '0xaf65h', profiles: [], merge: [], branches: {}	},
				// 						{	commit: '0xaf65g', profiles: [], merge: [], branches: {}	},
				// 						{	commit: '0xaf65f', profiles: [], merge: [], branches: {}	},
				// 						{	commit: '0xaf65e', profiles: [], merge: [], branches: {}	},
				// 						{	commit: '0xaf65e', profiles: [], merge: [], branches: {}	},
				// 						{	commit: '0xaf65e', profiles: [], branches: {}, merge: ['master']	},
				// 					],
				// 				},
				// 		},
				// 		{	commit: '0aaaa', profiles: [], merge: [], branches: {}	},
				// 		{	commit: '0aaaa', profiles: [], merge: [], branches: {}	},
				// 		{	commit: '0aaaa', profiles: [], merge: [], branches: {}	},
				// 		{	commit: '0xaf65a', profiles: [], merge: [],
				// 				branches: {
				// 					'bigfix2' : [
				// 						{	commit: '0xaf65a', profiles: [], merge: [], branches: {}	},
				// 						{	commit: '0xaf65a', profiles: [], merge: [], branches: {}	},
				// 						{	commit: '0xaf65a', profiles: [], merge: [], branches: {}	},
				// 						{	commit: '0xaf65a', profiles: [], merge: [], branches: {}	},
				// 					],
				// 				}
				// 		},
				// 	]
				// },
				// repo_local: {
				// 	master: [
				// 		{ commit: 'master01', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
				// 		{ commit: 'master02', profiles: [], mergeInto: '', mergeFrom: '', branches: ['bugfix1'] },
				// 		{ commit: 'master03', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
				// 		{ commit: 'master04', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
				// 		{ commit: 'master05', profiles: [], mergeInto: '', mergeFrom: 'bugfix1', branches: [] },
				// 		{ commit: 'master06', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
				// 	],
				// 	bugfix1: [
				// 		{ commit: 'bugfix101', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
				// 		{ commit: 'bugfix102', profiles: [], mergeInto: '', mergeFrom: '', branches: ['bugfix2'] },
				// 		{ commit: 'bugfix103', profiles: [], mergeInto: '', mergeFrom: 'bugfix2', branches: [] },
				// 		{ commit: 'bugfix104', profiles: [], mergeInto: 'master', mergeFrom: '', branches: [] },
				// 	],
				// 	bugfix2: [
				// 		{ commit: 'bugfix201', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
				// 		{ commit: 'bugfix202', profiles: [], mergeInto: 'bugfix1', mergeFrom: '', branches: [] },
				// 	],
				// },

				repoHistory: {
					master: [
						{ commit: 'master01', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'master02', profiles: [], mergeInto: '', mergeFrom: '', branches: ['bugfix1'] },
						{ commit: 'master03', profiles: [], mergeInto: 'bugfix1', mergeFrom: '', branches: [] }, //bugfix103
						{ commit: 'master04', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'master05', profiles: [], mergeInto: '', mergeFrom: 'bugfix1', branches: [] },
						{ commit: 'master06', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						// { level: 0, parentBranch: '' },
						// { commit: 'master07', profiles: [], mergeInto: 'bugfix1', mergeFrom: '', branches: [] },
						// { commit: 'master08', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						// { commit: 'master09', profiles: [], mergeInto: 'bugfix2', mergeFrom: '', branches: [] },
					],
					bugfix1: [
						{ commit: 'bugfix101', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'bugfix102', profiles: [], mergeInto: '', mergeFrom: 'master', branches: ['bugfix2'] }, //master03
						{ commit: 'bugfix103', profiles: [], mergeInto: '', mergeFrom: 'bugfix2', branches: [] }, 
						{ commit: 'bugfix104', profiles: [], mergeInto: '', mergeFrom: '', branches: [] }, ///tu
						{ commit: 'bugfix105', profiles: [], mergeInto: 'master', mergeFrom: '', branches: [] },
						{ commit: 'bugfix107', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'bugfix108', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'bugfix109', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						// { level: 1, parentBranch: 'master' }
					],
					bugfix2: [
						{ commit: 'bugfix201', profiles: [], mergeInto: '', mergeFrom: '', branches: ['bugfix3'] },
						{ commit: 'bugfix202', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'bugfix202', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'bugfix203', profiles: [], mergeInto: 'bugfix1', mergeFrom: '', branches: [] },
						// { level: 2, parentBranch: 'bugfix1' },
						// { commit: 'bugfix201', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
					],
					bugfix3: [
						{ commit: 'bugfix301', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'bugfix302', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						{ commit: 'bugfix303', profiles: [], mergeInto: '', mergeFrom: '', branches: [] },
						// { level : 3, parentBranch: 'bugfix2' },
					],
				},

				existingBranches: {},
				gitgraph: '', -->
<!-- myTemplateConfig: {
					graph: {
						orientation: "vertical",
					},
					colors: [ "#4DB6AC", "#607D8B", "#7E57C2", "#448AFF" ], // branches colors, 1 per column
					branch: {
						lineWidth: 5,
						spacingX: 35,
						showLabel: true,

						// mergeStyle: "straight",
						// labelFont: "normal 7pt sans-serif",
					},
					commit: {
						spacingY: -32,
						dot: {
						  size: 8,
						  color: "white",
						  strokeWidth: 3,
						},
						message: {
						  displayAuthor: false,
						  displayBranch: false,
						  displayHash: false,
						  messageDisplay: false,
						  font: "normal 10pt sans-serif"
						},
						shouldDisplayTooltipsInCompactMode: false, // default = true
						tooltipHTMLFormatter: function ( commit ) {
					  		return "" + commit.sha1 + "" + ": " + commit.message;
						}
				  	},
				}, -->