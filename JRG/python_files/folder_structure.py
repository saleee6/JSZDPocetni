from os import mkdir
from os.path import exists, dirname, join
from distutils.dir_util import copy_tree
import shutil
import JRG.python_files.folder_config as folder_config

this_folder = join(dirname(__file__), '..')
template_folder = join(this_folder, 'templates')
grammar_path = join(this_folder, 'grammar.tx')

def create_folders(base_dir, base_name):
    #region Folders

    base_folder = join(base_dir, base_name)

    #region Backend Folders

    folder_config.backend_folder = join(base_folder, 'demo')
    folder_config.backend_base_folder = join(folder_config.backend_folder,'src','main','java','com','example','demo')
    folder_config.backend_base_generated_folder = join(folder_config.backend_base_folder,'generated')

    folder_config.backend_generated_interface_folder = join(folder_config.backend_base_generated_folder,'interfaces')
    folder_config.backend_generated_controllers_folder = join(folder_config.backend_base_generated_folder,'controllers')
    folder_config.backend_generated_repositories_folder = join(folder_config.backend_base_generated_folder,'repositories')
    folder_config.backend_generated_service_folder = join(folder_config.backend_base_generated_folder,'services')
    folder_config.backend_generated_models_folder = join(folder_config.backend_base_generated_folder,'models')
    folder_config.backend_generated_dtos_folder = join(folder_config.backend_base_generated_folder,'dtos')

    folder_config.backend_interface_folder = join(folder_config.backend_base_folder,'interfaces')
    folder_config.backend_controllers_folder = join(folder_config.backend_base_folder,'controllers')
    folder_config.backend_repositories_folder = join(folder_config.backend_base_folder,'repositories')
    folder_config.backend_service_folder = join(folder_config.backend_base_folder,'services')
    folder_config.backend_models_folder = join(folder_config.backend_base_folder,'models')
    folder_config.backend_dtos_folder = join(folder_config.backend_base_folder,'dtos')

    #endregion

    #region Frontend Folders

    folder_config.frontend_folder = join(base_folder, 'demo-app')
    folder_config.frontend_base_folder = join(folder_config.frontend_folder, 'src')

    folder_config.frontend_interface_folder = join(folder_config.frontend_base_folder,'interfaces')
    folder_config.frontend_components_folder = join(folder_config.frontend_base_folder,'components')
    folder_config.frontend_containers_folder = join(folder_config.frontend_base_folder,'containers')
    folder_config.frontend_service_folder = join(folder_config.frontend_base_folder,'services')
    folder_config.frontend_types_folder = join(folder_config.frontend_base_folder,'types')

    folder_config.frontend_generated_interface_folder = join(folder_config.frontend_interface_folder,'generated')
    folder_config.frontend_generated_components_folder = join(folder_config.frontend_components_folder,'generated')
    folder_config.frontend_generated_containers_folder = join(folder_config.frontend_containers_folder,'generated')
    folder_config.frontend_generated_service_folder = join(folder_config.frontend_service_folder,'generated')
    folder_config.frontend_generated_types_folder = join(folder_config.frontend_types_folder,'generated')

    #endregion

    #endregion

    if not exists(base_folder):
        mkdir(base_folder)

    #region Project/demo

    if not exists(folder_config.backend_folder):
        mkdir(folder_config.backend_folder)
        copy_tree(join(this_folder, 'demo'), folder_config.backend_folder)

    if not exists(folder_config.backend_base_generated_folder):
        mkdir(folder_config.backend_base_generated_folder)
    else:
        shutil.rmtree(folder_config.backend_base_generated_folder)
        mkdir(folder_config.backend_base_generated_folder)

    #region Generated backend

    if not exists(folder_config.backend_generated_service_folder):
        mkdir(folder_config.backend_generated_service_folder)

    if not exists(folder_config.backend_generated_repositories_folder):
        mkdir(folder_config.backend_generated_repositories_folder)

    if not exists(folder_config.backend_generated_models_folder):
        mkdir(folder_config.backend_generated_models_folder)

    if not exists(folder_config.backend_generated_interface_folder):
        mkdir(folder_config.backend_generated_interface_folder)

    if not exists(folder_config.backend_generated_controllers_folder):
        mkdir(folder_config.backend_generated_controllers_folder)

    if not exists(folder_config.backend_generated_dtos_folder):
        mkdir(folder_config.backend_generated_dtos_folder)
    
    #endregion

    #region User backend

    if not exists(folder_config.backend_service_folder):
        mkdir(folder_config.backend_service_folder)

    if not exists(folder_config.backend_repositories_folder):
        mkdir(folder_config.backend_repositories_folder)

    if not exists(folder_config.backend_models_folder):
        mkdir(folder_config.backend_models_folder)

    if not exists(folder_config.backend_interface_folder):
        mkdir(folder_config.backend_interface_folder)

    if not exists(folder_config.backend_controllers_folder):
        mkdir(folder_config.backend_controllers_folder)

    if not exists(folder_config.backend_dtos_folder):
        mkdir(folder_config.backend_dtos_folder)

    #endregion

    #endregion

    #region Project/demo-app

    if not exists(folder_config.frontend_folder):
        mkdir(folder_config.frontend_folder)
        copy_tree(join(this_folder, 'demo-app'), folder_config.frontend_folder)

    if not exists(folder_config.frontend_interface_folder):
        mkdir(folder_config.frontend_interface_folder)

    if not exists(folder_config.frontend_generated_interface_folder):
        mkdir(folder_config.frontend_generated_interface_folder)
    else:
        shutil.rmtree(folder_config.frontend_generated_interface_folder)
        mkdir(folder_config.frontend_generated_interface_folder)

    if not exists(folder_config.frontend_components_folder):
        mkdir(folder_config.frontend_components_folder)

    if not exists(folder_config.frontend_generated_components_folder):
        mkdir(folder_config.frontend_generated_components_folder)
    else:
        shutil.rmtree(folder_config.frontend_generated_components_folder)
        mkdir(folder_config.frontend_generated_components_folder)

    if not exists(folder_config.frontend_containers_folder):
        mkdir(folder_config.frontend_containers_folder)

    if not exists(folder_config.frontend_generated_containers_folder):
        mkdir(folder_config.frontend_generated_containers_folder)
    else:
        shutil.rmtree(folder_config.frontend_generated_containers_folder)
        mkdir(folder_config.frontend_generated_containers_folder)

    if not exists(folder_config.frontend_service_folder):
        mkdir(folder_config.frontend_service_folder)

    if not exists(folder_config.frontend_generated_service_folder):
        mkdir(folder_config.frontend_generated_service_folder)
    else:
        shutil.rmtree(folder_config.frontend_generated_service_folder)
        mkdir(folder_config.frontend_generated_service_folder)

    if not exists(folder_config.frontend_types_folder):
        mkdir(folder_config.frontend_types_folder)

    if not exists(folder_config.frontend_generated_types_folder):
        mkdir(folder_config.frontend_generated_types_folder)
    else:
        shutil.rmtree(folder_config.frontend_generated_types_folder)
        mkdir(folder_config.frontend_generated_types_folder)
    
    #endregion
