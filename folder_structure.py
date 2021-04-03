from os import mkdir
from os.path import exists, dirname, join
from distutils.dir_util import copy_tree
import shutil

this_folder = dirname(__file__)
base_folder = join(this_folder, 'project')

grammar_path = join(this_folder, 'grammar.tx')
example_path = join(this_folder, 'example.jszd')

#region Folders

#region Backend Folders

backend_folder = join(base_folder, 'demo')
backend_base_folder = join(backend_folder,'src','main','java','com','example','demo','generated')

backend_interface_folder = join(backend_base_folder,'interfaces')
controllers_folder = join(backend_base_folder,'controllers')
repositories_folder = join(backend_base_folder,'repositories')
backend_service_folder = join(backend_base_folder,'services')
models_folder = join(backend_base_folder,'models')
dtos_folder = join(backend_base_folder,'dtos')

#endregion

#region Frontend Folders

frontend_folder = join(base_folder, 'demo-app')
frontend_base_folder = join(frontend_folder, 'src')

frontend_interface_folder = join(frontend_base_folder,'interfaces')
components_folder = join(frontend_base_folder,'components')
containers_folder = join(frontend_base_folder,'containers')
frontend_service_folder = join(frontend_base_folder,'services')
types_folder = join(frontend_base_folder,'types')

generated_frontend_interface_folder = join(frontend_interface_folder,'generated')
generated_components_folder = join(components_folder,'generated')
generated_containers_folder = join(containers_folder,'generated')
generated_frontend_service_folder = join(frontend_service_folder,'generated')
generated_types_folder = join(types_folder,'generated')

#endregion

#endregion

def create_folders():
    if not exists(base_folder):
        mkdir(base_folder)

    #region Project/demo

    if not exists(backend_folder):
        mkdir(backend_folder)
        copy_tree(join(this_folder, 'demo'), backend_folder)

    if not exists(backend_base_folder):
        mkdir(backend_base_folder)
    else:
        shutil.rmtree(backend_base_folder)
        mkdir(backend_base_folder)

    if not exists(backend_service_folder):
        mkdir(backend_service_folder)

    if not exists(repositories_folder):
        mkdir(repositories_folder)

    if not exists(models_folder):
        mkdir(models_folder)

    if not exists(backend_interface_folder):
        mkdir(backend_interface_folder)

    if not exists(controllers_folder):
        mkdir(controllers_folder)

    if not exists(dtos_folder):
        mkdir(dtos_folder)
    
    #endregion

    #region Project/demo-app

    if not exists(frontend_folder):
        mkdir(frontend_folder)
        copy_tree(join(this_folder, 'demo-app'), frontend_folder)

    if not exists(frontend_interface_folder):
        mkdir(frontend_interface_folder)

    if not exists(generated_frontend_interface_folder):
        mkdir(generated_frontend_interface_folder)
    else:
        shutil.rmtree(generated_frontend_interface_folder)
        mkdir(generated_frontend_interface_folder)

    if not exists(components_folder):
        mkdir(components_folder)

    if not exists(generated_components_folder):
        mkdir(generated_components_folder)
    else:
        shutil.rmtree(generated_components_folder)
        mkdir(generated_components_folder)

    if not exists(containers_folder):
        mkdir(containers_folder)

    if not exists(generated_containers_folder):
        mkdir(generated_containers_folder)
    else:
        shutil.rmtree(generated_containers_folder)
        mkdir(generated_containers_folder)

    if not exists(frontend_service_folder):
        mkdir(frontend_service_folder)

    if not exists(generated_frontend_service_folder):
        mkdir(generated_frontend_service_folder)
    else:
        shutil.rmtree(generated_frontend_service_folder)
        mkdir(generated_frontend_service_folder)

    if not exists(types_folder):
        mkdir(types_folder)

    if not exists(generated_types_folder):
        mkdir(generated_types_folder)
    else:
        shutil.rmtree(generated_types_folder)
        mkdir(generated_types_folder)
    
    #endregion
