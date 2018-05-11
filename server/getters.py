from __future__ import print_function
import os, sys, json
import collections
from shutil import rmtree

from flask import Response, jsonify

import perun.vcs as vcs
import perun.logic.commands as commands
import perun.cli as cli
import perun.logic.config as config
import perun.logic.runner as runner
from perun.logic.pcs import pass_pcs
import perun.profile.factory as profile
import perun.profile.query as query
import perun.profile.convert as convert
import perun.check as check
import pandas as pandas

import formatters as formatter


def eprint(*args, **kwargs):
    """Helper function for printing to stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def tidy_path(path):
    """Helper function for formatting a path
    :param str path: path to be formatted
    :return: formatted path
    """
    if (not path.startswith('/')):
        path = '/' + path
    if (not path.endswith('/')):
        path += '/'
    return path

def create_response(message, ret_status):
    response = jsonify({'message': str(message)})
    response.status_code = ret_status
    return response

def check_perun_integration(subdirs):
    """Helper function for determining the existence of perun wrapper over the underlaying vcs
    :param str subdirs: list of subdirectories located in the repository
    :return: str depending on the status
    """
    for name in subdirs:
        if name == '.perun':
            return 'integrated'

    return 'missing'

def get_repos_from_path(vcs_type, path_to_search):
    """Function for traversing the user-specified path, searching for repositories
    :param str vcs_type: type of vcs to be looking for
    :param str path_to_search: path from which the search is to be commenced
    :return: list of dicts containing repositories
    """
    try:
        if os.path.isdir(path_to_search):

            repos = []
            for dirname, dirnames, filenames in os.walk(path_to_search):
                for subdirname in dirnames:
                    if subdirname == ('.' + vcs_type):
                        if (dirname.endswith('/')):
                            tmp_path = dirname[:-1]
                        else:
                            tmp_path = dirname

                        repos.append(formatter.format_repo_info(os.path.basename(tmp_path), dirname, vcs_type, check_perun_integration(dirnames)))

            return jsonify({'repositories' : repos})
        else:
            return create_response('Invalid path', 404)

    except Exception as e:
        eprint(e)
        return create_response('Invalid path', 404)

@pass_pcs
def create_perun_instance(pcs, repo_path, vcs_type): #/home/parallels/Desktop/test-one
    """Function creating a Perun wrapper over the specified repository
    :param PCS pcs: object with performance control system wrapper
    :param str repo_path: path to the repo
    :param str vcs_type: type of vcs to be looking for
    :return: status depending whether the operation was successfull or not
    """
    try:
        if os.path.isdir(repo_path):
            commands.init(repo_path, **{
                'vcs_type': vcs_type,
                'vcs_path': repo_path,
                'vcs_params': ''
            })
            return create_response('All ok', 200)
        else:
            return create_response('Invalid path', 404)

    except Exception as e:
        eprint(e)
        return create_response(e, 404)

def remove_perun_instance(repo_path):
    """Function removing a Perun wrapper over the specified repository
    :param str repo_path: path to the repo
    :return: status depending whether the operation was successfull or not
    """
    try:
        if os.path.isdir(repo_path + '/.perun'):
            rmtree(repo_path + '/.perun')
            return create_response('All ok', 200)
        else:
            return create_response('Invalid path', 404)

    except Exception as e:
        eprint(e)
        return create_response(e, 404)

# def get_minor_versions_of_branch(vcs_type, repo_path):
#     """Function for loading minor versions of a branch, currently only the major branch
#     :param str vcs_type: type of the version control system
#     :param str path_to_repo: path to the repository
#     :return: list of minor versions on success, otherwise 404 NOT FOUND
#     """
#     if os.path.isdir(repo_path):
#         minor_versions = []
#         head = vcs.get_minor_head(vcs_type, repo_path)

#         for minor_version in vcs.walk_minor_versions(vcs_type, repo_path, head):
#             minor_versions.append(formatter.format_minor_versions_of_branch(minor_version, '', False))

#         return minor_versions

#     else:
#         return NOT_FOUND

# get_minor_versions_of_branch('git','/home/parallels/Desktop/BP/git-test-dir')

def get_repo_branch_names(vcs_type, repo_path):
    """Function for loading major versions of a repository
    :param str vcs_type: type of the version control system
    :param str repo_path: path to the repository
    :return: list of major versions
    """
    branches = []
    try:
        major_versions = vcs.walk_major_versions(vcs_type, repo_path)
        for branch in major_versions:
            branches.append(branch.name)

        return jsonify({'optionalBranches' : branches})

    except Exception as e:
        eprint(e)
        return create_response(e, 404)

def helper_get_repo_branch_commits(vcs_type, repo_path, branch_name):
    """Function for loading all minor versions of a given branch
    :param str vcs_type: type of the version control system
    :param str repo_path: path to the repository
    :param str branch_name: name of the branch
    :return: list of minor versions
    """

    major_versions = vcs.walk_major_versions(vcs_type, repo_path)
    output = []
    
    for branch in major_versions:
        if (branch.name == branch_name):
            for minor_version in vcs.walk_minor_versions(vcs_type, repo_path, branch.head):
                output.append(minor_version)

    return output


@pass_pcs
def get_repo_branch_commits(pcs, vcs_type, repo_path, branch_name):
    """Function for loading information about all commits of a branch
    :param PCS pcs: object with performance control system wrapper
    :param str vcs_type: type of the version control system
    :param str repo_path: path to the repository
    :param str branch_name: name of the branch
    :return: list of minor versions info
    """
    output = []

    try:
        minor_versions = helper_get_repo_branch_commits(vcs_type, repo_path, branch_name)

        branches = vcs.walk_major_versions(vcs_type, repo_path)
        for branch in branches:
            if (branch.name == branch_name):
                branch_head = branch.head

        for minor_version in minor_versions:
            head = 'head' if (minor_version.checksum == branch_head) else ''

            degs = check.count_degradations_per_group(check.load_degradation_list_for(pcs.get_object_directory(), minor_version.checksum))
            degs = formatter.format_degradation_numbers(degs)

            profiles = commands.get_minor_version_profiles(pcs, minor_version.checksum);
            profile_numbers = commands.calculate_profile_numbers_per_type(profiles)
            
            numbers = {
                'time': 0,
                'memory': 0,
                'mixed': 0,
                'all': 0,
            }

            for key,number in profile_numbers.items():
                numbers[str(key)] = number

            output.append(formatter.format_minor_versions_of_branch(minor_version, branch_name, head, numbers, degs))

        return output, json.dumps({'commits' : output})

    except Exception as e:
        eprint(e)
        return '', create_response(e, 404)

# def get_branch_commit_info(vcs_type, vcs_path, branch_name, minor_version):
#     """Function for loading minor version information
#     :param str vcs_type: type of the version control system
#     :param str vcs_path: path to the repository
#     :param str minor_version_sha: minor version SHA
#     :return: dictionary with minor version data
#     """
#     minor_version = vcs.get_minor_version_info(vcs_type, vcs_path, minor_version)
#     return formatter.format_single_minor_version_info(minor_version, branch_name)

def get_single_minor_version_info(vcs_type, vcs_path, minor_version_sha):
    """Function for loading minor version information
    :param str vcs_type: type of the version control system
    :param str vcs_path: path to the repository
    :param str minor_version_sha: minor version SHA
    :return: dictionary with minor version data
    """
    try:
        minor_version = vcs.get_minor_version_info(vcs_type, vcs_path, minor_version_sha)
        return jsonify({'commit': formatter.format_single_minor_version_info(minor_version, '')})
    
    except Exception as e:
        eprint(e)
        return create_response(e, 404)

# def dump(obj):
#    for attr in dir(obj):
#        if hasattr( obj, attr ):
#            print( "obj.%s = %s" % (attr, getattr(obj, attr)))

@pass_pcs
def get_single_minor_version_profiles(pcs, minor_version, branch_name):
    """Function for loading performance profiles of a single minor version
    :param PCS pcs: object with performance control system wrapper
    :param str minor_version: minor version SHA
    :return: list of performance profiles
    """
    output = []
    output_objs = []

    try:
        # registered profiles
        profiles_objs = commands.get_minor_version_profiles(pcs, minor_version);
        for num, profile_obj in enumerate(profiles_objs):
            output.append(formatter.format_profiles(profile_obj, minor_version, True, 'remove', branch_name))
            output_objs.append(profile_obj)

        # pending profiles
        profiles_objs = commands.get_untracked_profiles(pcs);
        for num, profile_obj in enumerate(profiles_objs):
            unpacked_profile = profile.load_profile_from_file(profile_obj.realpath, is_raw_profile=True)
            if (unpacked_profile['origin'] == minor_version):
                output.append(formatter.format_profiles(profile_obj, minor_version, False, 'register', branch_name))
                output_objs.append(profile_obj)

        return output_objs, output, json.dumps({'profiles' : output})

    except Exception as e:
        eprint(e)
        return '', '', create_response(e, 404)

@pass_pcs
def get_all_repo_profiles(pcs, vcs_type, repo_path):
    """Function for loading performance profiles of the whole repository
    :param PCS pcs: object with performance control system wrapper
    :param str vcs_type: type of the version control system
    :param str vcs_path: path to the repository
    :return: list of performance profiles
    """
    output = []
    output_objs = []
    try: 
        major_versions = vcs.walk_major_versions(vcs_type, repo_path)

        for branch in major_versions:
            minor_versions = helper_get_repo_branch_commits(vcs_type, repo_path, branch.name)
            for commit in minor_versions:
                objs, profiles, profiles_json = get_single_minor_version_profiles(commit.checksum, branch.name)
                for perf_profile in profiles:
                    if not any(d['id'] == perf_profile['id'] for d in output):
                        output.append(perf_profile)
                
                for perf_profile_obj in objs:
                    if (not any(x for x in output_objs if x.source == perf_profile_obj.source)):
                        output_objs.append(perf_profile_obj)

        return output_objs, output, json.dumps({'profiles' : output})

    except Exception as e:
        eprint(e)
        return '', '', create_response(e, 404)

@pass_pcs
def register_profile_of_minor_version(pcs, minor_version, profile_path, profile_id):
    """Function for registering performance profile of a minor version
    :param PCS pcs: object with performance control system wrapper
    :param str minor_version_sha: minor version SHA
    :param str profile_path: path to the performance profile
    :param str profile_id: name of the performance profile
    :return: new profile path on success, otherwise 404 NOT FOUND
    """
    try: 
        commands.add([profile_path], minor_version, keep_profile=False)
        profiles = commands.get_minor_version_profiles(pcs, minor_version);
        for perf_profile in profiles:
            if (perf_profile.source == profile_id):
                return jsonify({'path' : perf_profile.realpath})

        return create_response('No such performance profile', 404)
    
    except Exception as e:
        eprint(e)
        return create_response(e, 404)

def unregister_profile_of_minor_version(minor_version, profile_name):
    """Function for registering performance profile of a minor version
    :param PCS pcs: object with performance control system wrapper
    :param str profile_name: name of the performance profile
    :return: new profile path
    """
    try:
        commands.remove([profile_name], minor_version)
        return create_response('Unregistering successfull', 200)
    
    except Exception as e:
        eprint(e)
        return create_response(e, 404)

@pass_pcs
def get_single_profile_info(pcs, minor_version, profile_source):
    """Function for loading single performance profile info
    :param PCS pcs: object with performance control system wrapper
    :param str minor_version: commit to which the profiles belongs
    :param str profile_source: name of the performance profile
    :return: dictionary containing performance profile info
    """
    try:
        profiles_objs = commands.get_minor_version_profiles(pcs, minor_version);
        for num, profile_obj in enumerate(profiles_objs):
            if (profile_obj.source == profile_source):
                perf_profile = profile.load_profile_from_file(profile_obj.realpath, is_raw_profile=False)
                options = [o for o in query.all_resource_fields_of(perf_profile)]
                numerical = [o for o in query.all_numerical_resource_fields_of(perf_profile)]
                dataframe = convert.resources_to_pandas_dataframe(perf_profile)

                for option in options:
                    dataframe = dataframe[pandas.notnull(dataframe[option])]
                
                dataframe = dataframe.astype(str)
                resource_values = dataframe.to_dict(orient='records')

                formatted = formatter.format_single_profile_info(profile_obj, minor_version, options, numerical, resource_values)

                return formatted, json.dumps({'profile' : formatted})

        profiles_objs = commands.get_untracked_profiles(pcs);
        for num, profile_obj in enumerate(profiles_objs):
            if (profile_obj.source == profile_source):
                perf_profile = profile.load_profile_from_file(profile_obj.realpath, is_raw_profile=True)
                options = [o for o in query.all_resource_fields_of(perf_profile)]
                numerical = [o for o in query.all_numerical_resource_fields_of(perf_profile)]
                dataframe = convert.resources_to_pandas_dataframe(perf_profile)
                
                for option in options:
                    dataframe = dataframe[pandas.notnull(dataframe[option])]

                dataframe = dataframe.astype(str)
                resource_values = dataframe.to_dict(orient='records')

                formatted = formatter.format_single_profile_info(profile_obj, minor_version, options, numerical, resource_values)
                
                return formatted, json.dumps({'profile' : formatted})

        return create_response('Something went wrong', 404)

    except Exception as e:
        eprint(e)
        return create_response(e, 404)

def get_global_config():
    """Function for loading shared (global) Perun settings
    :return: dictionary containing global settings
    """
    try:
        global_settings = config.shared()
    except Exception as e:
        return create_response(e, 404)

    output = { 
        'general': [], 
        'format': [], 
    }

    items = {
        'general': ['paging','editor'],
        'format': ['status','log','output_profile_template'],
    }

    for section, item in items.items():
        for subsection in item:
            try:
                value = global_settings.get(section + '.' + subsection)
            except:
                value = ''
            finally:
                output[section].append(formatter.format_configuration(subsection, value, '', '', 'edit'))

    return jsonify({'globalSettings': output})   

def get_local_config(path_to_repo):
    """Function for loading shared (global) Perun settings
    :param str path_to_repo: path to repository
    :return: dictionary containing local settings
    """
    try:
        local_settings = config.local(path_to_repo + '/.perun')
    except Exception as e:
        eprint(e)
        return create_response(e, 404)

    output = { 
        'general': [], 
        'format': [],
        'vcs': [],
        'jobMatrix': {
            'profiledCommands': {
                'commands': [],
                'arguments': [],
                'workload': [],
            },
            'collectionSpecification': {
                'collectors': [],
                'postprocessors': [],
            },
        },
    }

    items = {
        'general': ['paging','editor'],
        'format': ['status','log','output_profile_template'],
        'vcs': ['type']
    }

    for section, item in items.items():
        for subsection in item:
            try:
                value = local_settings.get(section + '.' + subsection)
                nearest = ''
            except:
                try:
                    nearest = config.lookup_key_recursively(section + '.' + subsection)
                    value = ''
                except:
                    value = ''
                    nearest = '-----'
            finally:
                if (subsection == "type"):
                    output[section].append(formatter.format_configuration(subsection, value, nearest, path_to_repo, 'edit'))
                else:
                    output[section].append(formatter.format_configuration(subsection, value, nearest, '', 'edit'))

    hooks = { 
        'name': 'perun hooks',
        'type': 'checkbox',
        'actions': {
            "automatically generate profiles after" : [
                { "each commit": True },
                { "each push": False },
                { "each profile registration": False },
            ],
            "automatically detect degradation after" : [
                { "each commit": False },
                { "each push": True },
                { "each profile registration": False },
            ]
       }
    }

    output['vcs'].append(hooks)

    jm_items = {'cmds':[], 'args':[], 'workloads':[], 'collectors':[], 'postprocessors':[]}

    for section in jm_items:
        try:
            jm_items[section] = local_settings.get(section)
        except:
            jm_items[section] = []
    
    output['jobMatrix']['profiledCommands']['commands'] = jm_items['cmds']
    output['jobMatrix']['profiledCommands']['arguments'] = jm_items['args']
    output['jobMatrix']['profiledCommands']['workload'] = jm_items['workloads']
    output['jobMatrix']['collectionSpecification']['collectors'] = formatter.format_job_matrix_unit(jm_items['collectors'])
    output['jobMatrix']['collectionSpecification']['postprocessors'] = formatter.format_job_matrix_unit(jm_items['postprocessors'])

    return jsonify({'localSettings': output})

def set_global_settings(section, name, value):
    """Function for setting shared (global) Perun settings
    :param str section: section of settings which contains the specified command (eg. general)
    :param str name: name of the item which is to be set (eg. paging)
    :param str value: new value
    :return: 200 OK if successfull, 404 NOT FOUND otherwise
    """
    try:
        commands.config_set('shared', section + '.' + name, value)
        return create_response('Global settings set successfully', 200)
    
    except Exception as e:
        eprint(e)
        return create_response(e, 404)

def set_local_settings(path_to_repo, section, name, value):
    """Function for setting local Perun settings
    :param str path_to_repo: path to repository
    :param str section: section of settings which contains the specified command (eg. general)
    :param str name: name of the item which is to be set (eg. paging)
    :param str value: new value
    :return: 200 OK if successfull, 404 NOT FOUND otherwise
    """
    original_path = os.getcwd()
    os.chdir(path_to_repo)
    try:
        commands.config_set('local', section + '.' + name, value)
        os.chdir(original_path)
        return create_response('Local settings set successfully', 200)
    
    except Exception as e:
        os.chdir(original_path)
        eprint(e)
        return create_response(e, 404)

def collect_profile_using_job_matrix(vcs_type, repo_path, minor_version):
    """Function for collecting new profiles using predefined job matrix from local.yml
    :param str path_to_repo: path to repository
    :param str minor_version: commmit on which the collection is to be performed
    :return: list of performance profiles belonging to the specidied minor version
    """
    try:
        original_path = os.getcwd()
        os.chdir(repo_path)
        minor_version_obj = vcs.get_minor_version_info(vcs_type, repo_path, minor_version)
        runner.run_matrix_job([minor_version_obj])
        objs, output, jsn = get_single_minor_version_profiles(minor_version, '')
        os.chdir(original_path)
        return jsonify({'profiles': output})
    
    except Exception as e:
        os.chdir(original_path)
        eprint(e)
        return create_response(e, 404)


# collect_profile_using_job_matrix('git', '/home/parallels/Desktop/git-map', 'b159ba73b7c35bd1166187f583f1b90c835560f5')

def set_job_matrix_settings(repo_path, specification):
    """Function for setting job matrix settings
    :param str path_to_repo: path to repository
    :param dict specification: dictionary containging section, name and setting value
    :return: 200 OK if successfull, 404 NOT FOUND otherwise
    """
    try: 
        if (specification['section'] == 'collectionSpecification'):
            output = formatter.format_job_matrix_collection_specification(specification)
            name = specification['name']
        else:
            output = specification['value']

            if (specification['name'] == 'commands'):
                name = 'cmds'
            elif (specification['name'] == 'arguments'):
                name = 'args'
            elif (specification['name'] == 'workload'):
                name = 'workloads'

        original_path = os.getcwd()
        os.chdir(repo_path)
        commands.config_set('local', name, output)
        os.chdir(original_path)
        return create_response('Job matrix settings set successfully', 200)
    
    except Exception as e:
        os.chdir(original_path)
        eprint(e)
        return create_response(e, 404)

def performance_profile_postprocess(repo_path, profile_realpath, specification, registered):
    """Function for postprocessing the given profile with a postprocessor given by specification
    :param str repo_path: path to repository
    :param str profile_realpath: path to profile
    :param dict specification: dictionary containging postprocessor specification
    :param bool registered: registration status of the profile
    :return: 200 OK if successfull, 404 NOT FOUND otherwise
    """
    original_path = os.getcwd()
    os.chdir(repo_path)

    # if (registered):
    #     raw = False
    # else:
    #     raw = True

    try:
        perf_profile = profile.load_profile_from_file(profile_realpath, is_raw_profile=(not registered))
        
        name = ''
        arguments = ''

        if (specification['name'].lower() == 'regression analysis'):
            name = 'regression_analysis'
            arguments = {'method': '', 'regression_models': '', 'steps': '', 'of_key': '', 'per_key': ''}
            for param in specification['parameters']:
                if (param['param'] == 'method'):
                    arguments['method'] = param['options'][0]
                elif (param['param'] == 'regression models'):
                    arguments['regression_models'] = param['options']
                elif (param['param'] == 'steps'):
                    arguments['steps'] = param['options'][0]
                elif (param['param'] == 'of'):  
                    arguments['of_key'] = param['options'][0]
                elif (param['param'] == 'depending on'):
                    arguments['per_key'] = param['options'][0]
        
        elif (specification['name'].lower() == 'normalizer'):
            arguments = {}
            name = 'normalizer'
        elif (specification['name'].lower() == 'filter'):
            arguments = {}
            name = 'filter'
        
        runner.run_postprocessor_on_profile(perf_profile, name, arguments)
        os.chdir(original_path)
        return create_response('Profile postprocessed successfully', 200)

    except Exception as e:
        os.chdir(original_path)
        eprint(e)
        return create_response(e, 404)

def get_performance_profiles_list(repo_path, vcs_type, compare_profile):
    """Function for loading a performance profile list
    :param str repo_path: path to repository
    :param str vcs_type: type of underlying vcs
    :param str compare_profile: baseline profile SHA
    :return: json containing performance profiles list, 404 NOT FOUND otherwise
    """
    original_path = os.getcwd()
    try:
        os.chdir(repo_path)
        objs, profiles, jsn = get_all_repo_profiles('git', repo_path)
        output = []
        for perf_profile in profiles:
            if (compare_profile != perf_profile['id']):
                output.append({'id': perf_profile['id'], 'path': perf_profile['path'], 'commit': perf_profile['commit']})

        return json.dumps({'profiles': output})

    except Exception as e:
        os.chdir(original_path)
        eprint(e)
        return create_response(e, 404)


def get_profiles_to_compare(repo_path, baseline, target):
    """Function for loading two profiles which are to be compared
    :param str repo_path: path to repository
    :param dict baseline: dictionary containing baseline profile info
    :param dict baseline: target containing baseline profile info
    :return: json containing performance profiles info, 404 NOT FOUND otherwise
    """
    output = {'baseline': '', 'target': ''}
    original_path = os.getcwd()
    
    try:
        os.chdir(repo_path)
        output['baseline'], jsn = get_single_profile_info(baseline['commit'], baseline['id'])
        output['target'], jsn = get_single_profile_info(target['commit'], target['id'])
        os.chdir(original_path)
        return json.dumps({'profiles': output})

    except Exception as e:
        os.chdir(original_path)
        eprint(e)
        return create_response(e, 404)

@pass_pcs
def get_profiles_numbers(pcs, repo_path, vcs_type):
    """Function for loading two profiles which are to be compared
    :param PCS pcs: object with performance control system wrapper
    :param str repo_path: path to repository
    :param str vcs_type: type of underlying vcs
    :return: njson containing numbers of profile types and degradation info, 404 NOT FOUND otherwise
    """
    original_path = os.getcwd()
    os.chdir(repo_path)

    try:
        branches = vcs.walk_major_versions(vcs_type, repo_path)
        branches_output = []

        for branch in branches:
            profiles = commands.get_minor_version_profiles(pcs, branch.head);
            profile_numbers = commands.calculate_profile_numbers_per_type(profiles)

            numbers = {
                'time': 0,
                'memory': 0,
                'mixed': 0,
                'all': 0,
            }

            for key,number in profile_numbers.items():
                numbers[str(key)] = number

            degs = check.count_degradations_per_group(check.load_degradation_list_for(pcs.get_object_directory(), branch.head))
            degs = formatter.format_degradation_numbers(degs)

            branches_output.append({ 'branch' : branch.name, 'commit': branch.head, 'profiles': numbers, 'performance': degs})

        profiles_new, formatted, jsn = get_all_repo_profiles('git', repo_path)
        profile_numbers = commands.calculate_profile_numbers_per_type(profiles_new)

        numbers = {
            'time': 0,
            'memory': 0,
            'mixed': 0,
            'all': 0,
        }

        for key,number in profile_numbers.items():
            numbers[str(key)] = number

        os.chdir(original_path)
        return json.dumps({'all': numbers, 'branches': branches_output})

    except Exception as e:
        os.chdir(original_path)
        eprint(e)
        return create_response(e, 404)
