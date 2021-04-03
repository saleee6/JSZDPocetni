import jinja2
from datetime import datetime
from metamodel import SimpleType
from folder_structure import *

template_folder = join(this_folder, 'templates')

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
    if hasattr(p, 'constraints'):
        for constraint in p.constraints:
            if constraint.type == 'NotNullable':
                return True
    return False

def initial_value(property):
    """
    Return inital value based on property type.
    """
    if property.type.name == 'string':
        return '\'\''
    elif property.type.name == 'boolean':
        return 'false'
    else:
        return 0

def constraint_type(constraint):
    """
    Return constraint type.
    """
    if  constraint.type=='Length':
        return '.length('+ str(constraint.value) + ',\'Property must be ' + str(constraint.value) + ' characters long\')'
    elif constraint.type=='NotNullable':
        return '.required(\'Property is required \')'
    else:
        return ''

def property_constraint(constraint):
    """
    Return constraint for backend.
    """
    if constraint.type == 'NotNullable':
        return 'nullable=false'
    elif constraint.type == 'Unique':
        return 'unique=true'
    else:
        return constraint.type.lower() + '=' + str(constraint.value)

def property_decorator(decorator):
    """
    Return decorator for backend.
    """
    return decorator.type.lower() + '=' + decorator.type + 'Type.' + decorator.value

def join_table(property):
    """
    Return join expression for property.
    """
    if hasattr(property, 'join_table'):
        return '@JoinTable(name = "' + property.join_table + '", joinColumns=@JoinColumn(name = "' + property.name + '_id"), inverseJoinColumns=@JoinColumn(name = "' + property.related_name + '_id"))'
    else:
        return ''

#endregion

def generate_template_and_code(entity_model):
    jinja_backend_env, jinja_frontend_env = generate_template()
    generate_code(entity_model, jinja_backend_env, jinja_frontend_env)

def generate_template():
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
    jinja_backend_env.filters['property_constraint'] = property_constraint
    jinja_backend_env.filters['property_decorator'] = property_decorator
    jinja_backend_env.filters['join_table'] = join_table

    # Register filters for frontend engine
    jinja_frontend_env.filters['jstype'] = jstype
    jinja_frontend_env.filters['isSimpleType'] = isSimpleType
    jinja_frontend_env.filters['uncapitalize'] = uncapitalize
    jinja_frontend_env.filters['return_plural'] = return_plural
    jinja_frontend_env.filters['isRequired'] = isRequired
    jinja_frontend_env.filters['initial_value'] = initial_value
    jinja_frontend_env.filters['constraint_type'] = constraint_type

    return jinja_backend_env, jinja_frontend_env


def generate_code(entity_model, jinja_backend_env, jinja_frontend_env):
    #region Templates

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

    #endregion

    #region Generate code

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(join(generated_components_folder,
                        "NavBar.tsx"), 'w') as f:
            f.write(navbar_template.render(entities=entity_model.entities, time=dt_string))
    with open(join(generated_types_folder,
                        "Types.ts"), 'w') as f:
            f.write(types_template.render(entities=entity_model.entities, time=dt_string))

    for entity in entity_model.entities:
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

    #endregion
