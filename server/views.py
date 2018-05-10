from flask import render_template, jsonify, request
from app import app
import os, sys, json

from getters import *

vcs_type = 'git'
current_path = ''


@app.route('/repos/<path:path_to_search>', methods=['GET'])
def get_repos(path_to_search):
    """Function for initializing the search for repos on given path
    :param str path_to_search: path from which the search is to be started
    :return: 200 OK if path_to_search is a valid directory, 404 NOT FOUND otherwise
    """
    return get_repos_from_path(vcs_type, tidy_path(path_to_search))


@app.route('/repos/<path:path_to_repo>/integrate', methods=['PATCH'])
def integrate_repo(path_to_repo):
    """Function for initialization of creating the Perun wrapper over the given repository
    :param str path_to_repo: path to the repository
    :return: 200 OK if integration was successfull, 404 NOT FOUND otherwise
    """
    return create_perun_instance(tidy_path(path_to_repo), vcs_type)


@app.route('/repos/<path:path_to_repo>/remove', methods=['PATCH'])
def remove_repo_integration(path_to_repo):
    """Function for intialization of removing the Perun wrapper over the given repository
    :param str path_to_repo: path to the repository
    :return: 200 OK if removing was successfull, 404 NOT FOUND otherwise
    """
    return remove_perun_instance(tidy_path(path_to_repo))


@app.route('/repos/<path:path_to_repo>/branches', methods=['GET'])
def get_branches(path_to_repo):
    """Function for loading a json of minor versions of the given repository
    :param str path_to_repo: path to the repository
    :return: json of minor versions on success, 404 NOT FOUND otherwise
    """
    return get_repo_branch_names(vcs_type, tidy_path(path_to_repo));


@app.route('/repos/<path:path_to_repo>/<string:branch_name>/commits', methods=['GET'])
def get_commits(path_to_repo, branch_name):
    """Function for loading a json of minor versions of the given repository
    :param str path_to_repo: path to the repository
    :return: json of minor versions on success, 404 NOT FOUND otherwise
    """
    original_path = os.getcwd()
    os.chdir(tidy_path(path_to_repo))
    ojbs, minor_versions = get_repo_branch_commits(vcs_type, tidy_path(path_to_repo), branch_name);
    os.chdir(original_path)
    return minor_versions


@app.route('/repos/<path:repo_path>/commits/<string:commit_id>/info', methods=['GET']) 
def get_commit_info(repo_path, commit_id):
    """Function for loading a information on the given minor version of the given repository
    :param str path_to_repo: path to the repository
    :param str commit_id: minor version SHA
    :return: json of information in success, 404 NOT FOUND otherwise
    """
    return get_single_minor_version_info(vcs_type, tidy_path(repo_path), commit_id)


@app.route('/repos/<path:repo_path>/profiles', methods=['GET']) 
def get_repo_profiles(repo_path):
    """Function for loading a json of all performance profiles of a repository
    :param str path_to_repo: path to the repository
    :return: json of performance profiles on success, 404 NOT FOUND otherwise
    """
    original_path = os.getcwd()
    os.chdir(tidy_path(repo_path))
    objs, formatted, profiles = get_all_repo_profiles(vcs_type, tidy_path(repo_path))
    os.chdir(original_path)
    return profiles


@app.route('/repos/<path:repo_path>/commits/<string:commit_id>/profiles', methods=['GET'])  #/home/parallels/Desktop/BP/git-test-dir
def get_commit_profiles(repo_path, commit_id):
    """Function for loading a json of performance profiles of the given minor version
    :param str path_to_repo: path to the repository
    :param str commit_id: minor version SHA
    :return: json of performance profiles on success, 404 NOT FOUND otherwise
    """
    original_path = os.getcwd()
    os.chdir(tidy_path(repo_path))
    objs, profiles_obj, profiles = get_single_minor_version_profiles(commit_id, '')
    os.chdir(original_path)
    return profiles


@app.route('/repos/<path:repo_path>/<string:commit_id>/profiles/<string:profile_id>/info', methods=['GET'])
def get_profile(repo_path, commit_id, profile_id):
    """Function for loading a json of a performance profile
    :param str repo_path: path to the repository
    :param str commit_id: minor version SHA
    :param str profile_id: name of the performace profile
    :return: json of performance profile on success, 404 NOT FOUND otherwise
    """
    original_path = os.getcwd()
    os.chdir(tidy_path(repo_path))
    obj, output = get_single_profile_info(commit_id, profile_id)
    os.chdir(original_path)
    return output


@app.route('/repos/<path:repo_path>/<string:commit_id>/profile-register', methods=['PATCH'])
def register_profile(repo_path, commit_id):
    """Function for initializing regsitration of a performance profile 
    :param str path_to_repo: path to the repository
    :param str commit_id: minor version SHA
    :return: on success json containing new path to the registered profile, otherwise 404 NOT FOUND
    """
    payload = request.get_json(force=True)
    original_path = os.getcwd()
    os.chdir(tidy_path(repo_path))
    new_path = register_profile_of_minor_version(commit_id, payload['path'], payload['id'])
    os.chdir(original_path)
    return new_path


@app.route('/repos/<path:repo_path>/<string:commit_id>/profile-unregister', methods=['PATCH'])
def unregister_profile(repo_path, commit_id):
    """Function for removing the registration of a performance profile 
    :param str path_to_repo: path to the repository
    :param str commit_id: minor version SHA
    :return: on success json containing new path to the registered profile, otherwise 404 NOT FOUND
    """
    payload = request.get_json(force=True)
    original_path = os.getcwd()
    os.chdir(tidy_path(repo_path))
    response = unregister_profile_of_minor_version(commit_id, payload['id'])
    os.chdir(original_path)
    return response


@app.route('/repos/<path:repo_path>/<string:commit_id>/job-matrix/collect-new', methods=['GET'])
def collect_new_profiles_job_matrix(repo_path, commit_id):
    """Function for triggering the collection of performance profiles based on job matrix specification
    :param str path_to_repo: path to the repository
    :param str commit_id: minor version SHA
    :return: json containing list of performance profiles
    """
    return collect_profile_using_job_matrix(vcs_type, tidy_path(repo_path), commit_id)


#TODO
@app.route('/repos/<path:repo_path>/<string:commit_id>/single-job/collect-new', methods=['GET'])
def collect_new_profiles(repo_path, commit_id):
    payload = request.get_json(force=True)
    original_path = os.getcwd()
    os.chdir(tidy_path(repo_path))
    profiles = jsonify({'profiles': new_collected_profiles})
    os.chdir(original_path)
    return profiles


@app.route('/repos/<path:repo_path>/profiles/<path:profile_path>/postprocess', methods=['PATCH'])
def postprocess_profile(repo_path, profile_path):
    """Function postprocessing the given performance profile
    :param str repo_path: path to the repository
    :param str profile_path: path to the performance profile
    :return: on success 200 OK, otherwise 404 NOT FOUND
    """
    payload = request.get_json(force=True)
    return performance_profile_postprocess(tidy_path(repo_path), profile_path, payload['specification'], payload['registration'])

@app.route('/global-settings', methods=['GET'])
def get_global_settings():
    """Function for loading the global configuration
    :return: json containong global configuration
    """
    return get_global_config()


@app.route('/global-settings/save', methods=['PATCH'])
def change_global_settings():
    """Function for changing the global configuration
    :return: 200 OK if successfull, 404 NOT FOUND otherwise
    """
    payload = request.get_json(force=True)
    return set_global_settings(payload['section'], payload['name'], payload['value'])


@app.route('/repos/<path:repo_path>/local-settings', methods=['GET'])
def get_local_settings(repo_path):
    """Function for loading the local configuration
    :param str repo_path: path to the repository
    :return: json containong local configuration
    """
    return get_local_config(tidy_path(repo_path))


@app.route('/repos/<path:repo_path>/local-settings/save', methods=['PATCH'])
def change_local_settings(repo_path):
    """Function for changing the local configuration
    :param str repo_path: path to the repository
    :return: 200 OK if successfull, 404 NOT FOUND otherwise
    """
    payload = request.get_json(force=True)
    return set_local_settings(tidy_path(repo_path), payload['section'], payload['name'], payload['value'])

@app.route('/repos/<path:repo_path>/local-settings/job-matrix/save', methods=['PATCH'])
def change_job_matrix_settings(repo_path):
    """Function for changing the job matrix settings
    :param str repo_path: path to the repository
    :return: 200 OK if successfull, 404 NOT FOUND otherwise
    """
    payload = request.get_json(force=True)
    return set_job_matrix_settings(tidy_path(repo_path), payload)

@app.route('/repos/<path:repo_path>/profiles/<string:profile_name>/list', methods=['GET'])
def get_all_profiles_list(repo_path, profile_name):
    """Function for loading a list of available performance profiles
    :param str repo_path: path to the repository
    :param str profile_name: name of the baseline performance profile
    :return: json containing list of performance profiles, 404 NOT FOUND otherwise
    """
    return get_performance_profiles_list(tidy_path(repo_path), vcs_type, profile_name)

@app.route('/repos/<path:repo_path>/profiles/compare', methods=['PATCH'])
def get_compare_profiles(repo_path):
    """Function for loading a list of available performance profiles
    :param str repo_path: path to the repository
    :return: json containing list of compared performance profiles, 404 NOT FOUND otherwise
    """
    payload = request.get_json(force=True)
    return get_profiles_to_compare(tidy_path(repo_path), payload['baseline'], payload['target'])

@app.route('/repos/<path:repo_path>/dashboard', methods=['GET'])
def get_dashboard(repo_path):
    """Function for loading dashboard data
    :param str repo_path: path to the repository
    :return: json containing dashboard data
    """
    original_path = os.getcwd()
    os.chdir(tidy_path(repo_path))
    output = get_profiles_numbers(tidy_path(repo_path), vcs_type)
    os.chdir(original_path)
    return output


@app.route('/', defaults = {'path': ''})
@app.route('/<path:path>')

def catch_all(path):
    return render_template("index.html")

def index():
    return render_template("index.html")
    