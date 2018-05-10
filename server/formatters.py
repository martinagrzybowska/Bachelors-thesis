def format_repo_info(vcs_name, vcs_path, vcs_type, integration_status):
    """Helper function for creating dict containing repository information
    :param str vcs_name: name of the repository
    :param str vcs_path: absolute path to the repository
    :param str vcs_type: type of the underlying vcs
    :param str integration_status: status of perun integration into the underlaying  vcs
    :return: dict containing repository information
    """
    return {
        'name' : vcs_name, 
        'path': vcs_path, 
        'vcs_type' : vcs_type,
        'integration': integration_status
    }

def format_minor_versions_of_branch(minor_version, branch_name, head, profiles, degradation):
    """Helper function for formating minor version data
    :param object minor_version: object containg minor version data
    :return: dictionary with minor version information
    """
    return {
        'minor_version': minor_version.checksum,
        'branch': branch_name,
        'head': head,
        'author': minor_version.author,
        'message': minor_version.desc,
        'date': minor_version.date,
        'profiles': profiles,
        'performance_info': degradation,
        'performance': 'degrading',
    }

def format_single_minor_version_info(minor_version, branch_name):
    """Helper function for formating minor version information
    :param object minor_version: object containg minor version data
    :return: dictionary with minor version data
    """
    return {
        # 'minor_version': minor_version.checksum,
        'author': minor_version.author,
        'message': minor_version.desc,
        'date': minor_version.date,
        'parents': minor_version.parents,
        'branch': branch_name,
    }

def format_profiles(profile_obj, origin, registered, action, branch_name): 
    """Helper function for formating performance profiles information
    :param object profile_obj: object containing performance profile data
    :param str origin: original minor version
    :param boolean registered: registration status of the profile
    :param str action: action depending on the registration status (either 'remove' of 'register')
    :return: dictionary with performance profile data
    """
    command = profile_obj.cmd + '/'
    if (profile_obj.args == ''):
        command += '---/'
    else:
        command += profile_obj.args + '/'

    if (profile_obj.workload == ''):
        command += '---'
    else :
        command += profile_obj.workload

    return {
        'registered': registered,
        'commit': origin,
        'branch': branch_name,
        'time': profile_obj.time,
        'command': command,
        'type': profile_obj.type,
        'collector': profile_obj.collector,
        'status': 'fill me',
        'action': action,
        'id': profile_obj.source,
        'path': profile_obj.realpath,
    }


def format_single_profile_info(profile, minor_version, options, numerical, resources):
    """Helper function for formating performance profile information
    :param object profile: object containing performance profile data
    :param str minor_version: original minor version
    :param list options: list of resource options
    :param dict resources: dictionary containing all resources
    :return: dictionary with performance profile data
    """
    return {
        'registered': not profile._is_raw_profile,
        'commit' : minor_version, 
        'profiled_command': [
            { 'path' : profile.realpath },
            { 'time of collection' : profile.time },
            { 'profile type' : profile.type },
            { 'command' : profile.cmd },
            { 'arguments' : profile.args },
            { 'workload' : profile.workload },
        ],
        'collection_configuration': [
            { 'collector' : profile.collector },
            { 'postprocessors' : profile.postprocessors },
        ],
        'chart_options': options,
        'chart_numerical_options': numerical,
        'resources': resources,
    }

def format_configuration(name, value, nearest, path, item_type):
    """Helper function for formating configuration output
    :param str name: name of the section being set, eg. paging or log
    :param str value: new value of the section
    :param str nearest: value of the nearest set section
    :param str path: path to the nearest set section
    :param str item_type: type of the setting, eg. blank, radio or edit
    :return: dictionary with configuration settings
    """
    name = name.replace('_', ' ')
    
    if (name == "paging"):
        item_type = "radio"
    elif (name == "type"):
        item_type = "blank"

    return {
        'name': name,
        'value': value,
        'nearest': nearest,
        'path': path,
        'type': item_type,  
    }

def format_job_matrix_unit(units):
    """Formatter function for formatting job matrix collector units and postprocessor units
    :param ????? units: 
    :return: dictionary containing formatted units information
    """
    output = []
    
    item = { 'name': '', 'parameters': [{ 'param': '', 'options': [] }]}
    
    for unit in units:
        name = unit['name']
        parameters = []
        try:
            for param in unit['params']:
                try: 
                    for option in param:
                        if isinstance(param[option],list):
                            parameters.append({'param': option, 'options': param[option]})
                        else:
                            parameters.append({'param': option, 'options': [param[option]]})
                except:
                    parameters.append({'param': param, 'options': []})
        except:
            parameters.append({'param': '', 'options': []})
        finally:
            output.append({'name': name, 'parameters': parameters})

    return output


def format_job_matrix_collection_specification(specification):
    """Formatter function for creating a format for new settings of job matrix
    :param dict specification: dictionary containging section, name and setting value
    :return: dictionary containing formatted units information
    """
    output = []
    
    for spec_item in specification['value']:
        item_format = {}
        item_format['name'] = spec_item['name']
        if ('parameters' in spec_item):
            item_format['params'] = []
            for parameter in spec_item['parameters']:
                if ('options' in parameter):
                    param_format = {}
                    if (len(parameter['options']) > 1):
                        options_format = []
                        for option in parameter['options']:
                            options_format.append(option)
                        
                        param_format[parameter['param']] = options_format
                    
                    else:
                        param_format[parameter['param']] = parameter['options'][0]

                    item_format['params'].append(param_format)

                else:
                    item_format['params'].append(parameter['param'])

        output.append(item_format)

    return output

def format_degradation_numbers(performance_dict):
    """Formatter function for creating a format for degradation information
    :param dict performance_dict: dictionary containging degradation information
    :return: dictionary containing formatted info
    """
    perf = {}
    perf['Degradation'] = performance_dict['Degradation'] if ('Degradation' in performance_dict) else 0
    perf['MaybeDegradation'] = performance_dict['MaybeDegradation'] if ('MaybeDegradation' in performance_dict) else 0
    perf['NoChange'] = performance_dict['NoChange'] if ('NoChange' in performance_dict) else 0
    perf['Unknown'] = performance_dict['Unknown'] if ('Unknown' in performance_dict) else 0
    perf['MaybeOptimization'] = performance_dict['MaybeOptimization'] if ('MaybeOptimization' in performance_dict) else 0
    perf['Optimization'] = performance_dict['Optimization'] if ('Optimization' in performance_dict) else 0
    return perf

















