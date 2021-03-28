from __future__ import unicode_literals
import os
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from textx import metamodel_from_file, TextXSemanticError
from textx.export import metamodel_export, model_export
from datetime import datetime
from distutils.dir_util import copy_tree
import shutil

this_folder = dirname(__file__)
base_folder = join(this_folder, 'project')
generarted_folder = join(this_folder, 'generated')
grammar_path = join(this_folder, 'grammar.tx')
template_folder = join(this_folder, 'templates')

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

class SimpleType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name

#region Validators
def relation_validator(property):
    if property.relation.type in ['ManyToOne','OneToOne'] and property.collectionType:
        raise TextXSemanticError('Relations ManyToOne and OneToOne can not be of type collection')

    if property.relation.type in ['OneToMany','ManyToMany'] and not property.collectionType:
        raise TextXSemanticError('Relations OneToMany and ManyToMany must be of type collection')

def decorator_validator(relation):
    if len(relation.decorators) != 0:
        for i in range(len(relation.decorators)):
            for j in range(i+1, len(relation.decorators)):
                if relation.decorators[i].type == relation.decorators[j].type:
                    raise TextXSemanticError('Can not have multiple decorators of the same type')

def constraint_validator(property):
    if len(property.constraints) != 0:
        for i in range(len(property.constraints)):
            for j in range(i+1, len(property.constraints)):
                if property.constraints[i].type == property.constraints[j].type:
                    raise TextXSemanticError('Can not have multiple constraints of the same type')

def length_constraint_validator(property):
    if len(property.constraints) != 0:
        for i in range(len(property.constraints)):
            if property.constraints[i].type == 'Length' and property.type.name != 'string':
                raise TextXSemanticError('Length constraint can only be set on property of type string')
#endregion

def get_entity_mm(debug=False):
    """
    Builds and returns a meta-model for Entity language.
    """
    type_builtins = {
        'int': SimpleType(None, 'int'),
        'string': SimpleType(None, 'string'),
        'bool': SimpleType(None, 'bool'),
        'float': SimpleType(None, 'float')
    }

    object_processors = {
        'ComplexRelationProperty' : relation_validator,
        'SimpleProperty' : constraint_validator,
        'SimpleProperty' : length_constraint_validator,
        'Relation' : decorator_validator
    }

    metamodel = metamodel_from_file(grammar_path,
                                    classes=[SimpleType],
                                    builtins=type_builtins,
                                    debug=debug)

    metamodel.register_obj_processors(object_processors)

    return metamodel

def main(debug=False):

    entity_mm = get_entity_mm(debug)

    #region Filters
    def javatype(s):
        """
        Maps type names from SimpleType to Java.
        """
        return {
                'string': 'String',
                'bool': 'boolean'
        }.get(s.name, s.name)

    def jstype(s):
        """
        Maps type names from SimpleType to JavaScript.
        """
        return {
                'bool': 'boolean',
                'int': 'number',
                'float': 'number'
        }.get(s.name, s.name)

    def isSimpleType(s):
        """
        Check property type.
        """
        return isinstance(s, SimpleType)

    def uncapitalize(s):
        """
        Change first letter to lowercase.
        """
        return s[0].lower() + s[1:]

    def return_plural(e):
        """
        Return plural of name.
        """
        if e.plural:
            return e.plural.value
        else:
            return e.name + 's'

    def isRequired(p):
        """
        Check if property is required.
        """
        for constraint in p.constraints:
            if constraint.type == 'NotNullable':
                return True
        return False
    #endregion

    # Create the output folder

    # Project
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

    # Template engine for backend
    jinja_backend_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(join(template_folder, 'backend')),
        trim_blocks=True,
        lstrip_blocks=True)

    # Template engine for frontend
    jinja_frontend_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(join(template_folder, 'frontend')),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filters for backend engine
    jinja_backend_env.filters['javatype'] = javatype
    jinja_backend_env.filters['isSimpleType'] = isSimpleType
    jinja_backend_env.filters['uncapitalize'] = uncapitalize
    jinja_backend_env.filters['return_plural'] = return_plural

    # Register filters for frontend engine
    jinja_frontend_env.filters['jstype'] = jstype
    jinja_frontend_env.filters['isSimpleType'] = isSimpleType
    jinja_frontend_env.filters['uncapitalize'] = uncapitalize
    jinja_frontend_env.filters['return_plural'] = return_plural
    jinja_frontend_env.filters['isRequired'] = isRequired

    # Load the Java templates for backend
    entity_template = jinja_backend_env.get_template('entity.template')
    repository_template = jinja_backend_env.get_template('repository.template')
    interface_backend_template = jinja_backend_env.get_template('interface.template')
    service_backend_template = jinja_backend_env.get_template('service.template')
    controller_template = jinja_backend_env.get_template('controller.template')
    dtos_template = jinja_backend_env.get_template('dto.template')

    # Load the Java templates for frontend
    navbar_template = jinja_frontend_env.get_template('navbar.template')
    preview_template = jinja_frontend_env.get_template('preview.template')
    types_template = jinja_frontend_env.get_template('types.template')
    interface_frontend_template = jinja_frontend_env.get_template('interface.template')
    popup_template = jinja_frontend_env.get_template('popup.template')
    service_frontend_template = jinja_frontend_env.get_template('service.template')

    # Export to .dot file for visualization
    dot_folder = join(this_folder, 'dotexport')
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)
    metamodel_export(entity_mm, join(dot_folder, 'grammar_meta.dot'))

    # Izgradnja modela u odnosu na konkretan primer
    entity_model = entity_mm.model_from_file(join(this_folder, 'example.jszd'))

    # Kreiranje .dot fajla u odnosu na izgradjeni model
    model_export(entity_model, join(dot_folder, 'example.dot'))

    # Generate Java code
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(join(generated_components_folder,
                      "NavBar.tsx"), 'w') as f:
            f.write(navbar_template.render(entities=entity_model.entities, time=dt_string))
    with open(join(generated_types_folder,
                      "Types.ts"), 'w') as f:
            f.write(types_template.render(entities=entity_model.entities, time=dt_string))

    for entity in entity_model.entities:
        # For each entity generate java file
        with open(join(models_folder,
                      "%s.java" % entity.name.capitalize()), 'w') as f:
            f.write(entity_template.render(entity=entity, time=dt_string))
        with open(join(repositories_folder,
                      "%sRepository.java" % entity.name.capitalize()), 'w') as f:
            f.write(repository_template.render(entity=entity, time=dt_string))
        with open(join(backend_interface_folder,
                      "%sInterface.java" % entity.name.capitalize()), 'w') as f:
            f.write(interface_backend_template.render(entity=entity, time=dt_string))
        with open(join(backend_service_folder,
                      "%sService.java" % entity.name.capitalize()), 'w') as f:
            f.write(service_backend_template.render(entity=entity, time=dt_string))
        with open(join(controllers_folder,
                      "%sController.java" % (entity.plural.value.capitalize() if entity.plural else (entity.name.capitalize() + 's'))), 'w') as f:
            f.write(controller_template.render(entity=entity, time=dt_string))
        with open(join(dtos_folder,
                      "%sDTO.java" % entity.name.capitalize()), 'w') as f:
            f.write(dtos_template.render(entity=entity, time=dt_string))
        with open(join(generated_containers_folder,
                      "%s.tsx" % (entity.plural.value.capitalize() if entity.plural else (entity.name.capitalize() + 's'))), 'w') as f:
            f.write(preview_template.render(entity=entity, time=dt_string))
        with open(join(generated_frontend_interface_folder,
                      "I%sPopup.ts" % entity.name.capitalize()), 'w') as f:
            f.write(interface_frontend_template.render(entity=entity, time=dt_string))
        with open(join(generated_components_folder,
                      "%sPopup.tsx" % entity.name.capitalize()), 'w') as f:
            f.write(popup_template.render(entity=entity, time=dt_string))
        with open(join(generated_frontend_service_folder,
                      "%sService.ts" % entity.name.capitalize()), 'w') as f:
            f.write(service_frontend_template.render(entity=entity, time=dt_string))


if __name__ == "__main__":
    main()