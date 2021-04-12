from textx import metamodel_from_file, TextXSemanticError
from os.path import dirname, join
from JRG.python_files.folder_structure import this_folder, grammar_path

#region Custom classes
class SimpleType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name

class CascadeDecorator(object):
    def __init__(self, parent, type, value):
        self.parent = parent
        self.type = type
        self.value = value

    def __str__(self):
        return self.type + ' ' + self.value

class FetchDecorator(object):
    def __init__(self, parent, type, value):
        self.parent = parent
        self.type = type
        self.value = value

    def __str__(self):
        return self.type + ' ' + self.value

#endregion

#region Validators
#region RelationProperty validators
def relation_validator(property):
    if property.relation.type in ['ManyToOne','OneToOne'] and property.collectionType:
        raise TextXSemanticError('Relations ManyToOne and OneToOne can not be of type collection')

    if property.relation.type in ['OneToMany','ManyToMany'] and not property.collectionType:
        raise TextXSemanticError('Relations OneToMany and ManyToMany must be of type collection')

#endregion

#region Relation validators
def decorator_validator(relation):
    if len(relation.decorators) != 0:
        for i in range(len(relation.decorators)):
            for j in range(i+1, len(relation.decorators)):
                if relation.decorators[i].type == relation.decorators[j].type:
                    raise TextXSemanticError('Can not have multiple decorators of the same type')

#endregion

#region Property validators
def property_id_validator(property):
    if property.name == 'id':
        raise TextXSemanticError('Property name can not be id')

def property_name_validator(property):
    if property.name == property.name.capitalize():
        raise TextXSemanticError('Property name "%s" must be uncapitalized.' % property.name)

def property_validator(property):
    property_id_validator(property)
    property_name_validator(property)

#endregion

#region ConstraintProperty validators
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

def constraint_property_validator(property):
    constraint_validator(property)
    length_constraint_validator(property)

#endregion

#region Entity validators
def unique_property_names_validator(entity):
    properties = []
    for property in entity.properties:
        if property.name in properties:
            raise TextXSemanticError('Property names must be unique within Entity')
        else:
            properties.append(property.name)

def entity_name_capitalize_validator(entity):
    if entity.name != entity.name.capitalize():
        raise TextXSemanticError('Entity name "%s" must be capitalized.' % entity.name)

def multiple_fields_same_entity_validator(entity):
    types = []
    for property in entity.properties:
        if not isinstance(property.type, SimpleType):
            if property.type.name in types:
                raise TextXSemanticError('You can not have multiple properties of the same entity type (This will be enabled in the future versions)')
            else:
                types.append(property.type.name)

def entity_property_validator(entity):
    for property in entity.properties:
        if not isinstance(property.type, SimpleType):
            if property.type.name == entity.name:
                raise TextXSemanticError('You can not have property of the same entity type as its containing entity (This will be enabled in the future versions)')

def one_to_many_many_to_one_validator(entity):
    for property in entity.properties:
        if not isinstance(property.type, SimpleType):
            if hasattr(property, 'relation'):
                if property.relation.type == 'OneToMany':
                    for related_property in property.type.properties:
                        if not isinstance(related_property.type, SimpleType):
                            if hasattr(related_property, 'relation'):
                                if related_property.type.name == entity.name:
                                    if related_property.relation.type != 'ManyToOne':
                                        raise TextXSemanticError(related_property.name + ' must be of complementary type ManyToOne')
                                    else:
                                        contains_cascade = False
                                        for decorator in property.relation.decorators:
                                            if decorator.type == 'Cascade':
                                                contains_cascade = True
                                                break
                                        if not contains_cascade:
                                            property.relation.decorators.append(CascadeDecorator(None, 'Cascade', 'ALL'))
                                        #property.relation.decorators.append(CascadeDecorator(None, 'mappedBy', related_property.name))
                elif property.relation.type == 'ManyToOne':
                    for related_property in property.type.properties:
                        if not isinstance(related_property.type, SimpleType):
                            if hasattr(related_property, 'relation'):
                                if related_property.type.name == entity.name:
                                    if related_property.relation.type != 'OneToMany':
                                        raise TextXSemanticError(related_property.name + ' must be of complementary type OneToMany')

def many_to_many_many_to_many_validator(entity):
    for property in entity.properties:
        if not isinstance(property.type, SimpleType):
            if hasattr(property, 'relation'):
                if property.relation.type == 'ManyToMany':
                    for related_property in property.type.properties:
                        if not isinstance(related_property.type, SimpleType):
                            if hasattr(related_property, 'relation'):
                                if related_property.type.name == entity.name:
                                    if related_property.relation.type != 'ManyToMany':
                                        raise TextXSemanticError(related_property.name + ' must be of complementary type ManyToMany')
                                    else:
                                        contains_cascade = False
                                        contains_fetch = False
                                        for decorator in property.relation.decorators:
                                            if decorator.type == 'Cascade':
                                                if decorator.value == 'PERSIST':
                                                    contains_cascade = True
                                                else:
                                                    raise TextXSemanticError(related_property.name + ' must have Cascade value PERSIST')
                                            if decorator.type == 'Fetch':
                                                if decorator.value == 'EAGER':
                                                    contains_fetch = True
                                                else:
                                                    raise TextXSemanticError(related_property.name + ' must have Fetch value EAGER')

                                        if not contains_cascade:
                                            property.relation.decorators.append(CascadeDecorator(None, 'Cascade', 'PERSIST'))
                                        if not contains_fetch:
                                            property.relation.decorators.append(FetchDecorator(None, 'Fetch', 'EAGER'))
                                        if not hasattr(property, 'join_table'):
                                            property.join_table = property.name + '_' + related_property.name
                                            related_property.join_table = property.name + '_' + related_property.name
                                            property.related_name = related_property.name
                                            related_property.related_name = property.name

def plural_validator(plural):
    if plural.value != plural.value.capitalize():
        raise TextXSemanticError('Plural value "%s" must be capitalized.' % plural.value)

def entity_validator(entity):
    entity_name_capitalize_validator(entity)
    unique_property_names_validator(entity)
    multiple_fields_same_entity_validator(entity)
    entity_property_validator(entity)
    one_to_many_many_to_one_validator(entity)
    many_to_many_many_to_many_validator(entity)

#endregion

#region EntityModel validators
def unique_entity_name_validator(entityModel):
    entities = []
    for entity in entityModel.entities:
        if entity.name in entities:
            raise TextXSemanticError('Entity names must be unique')
        else:
            entities.append(entity.name)

#endregion

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
        'EntityModel': unique_entity_name_validator,
        'Property': property_validator,
        'RelationProperty' : relation_validator,
        'ConstraintProperty' : constraint_property_validator,
        'Relation' : decorator_validator,
        'Entity': entity_validator,
        'Plural': plural_validator,
    }

    metamodel = metamodel_from_file(grammar_path,
                                    classes=[SimpleType, CascadeDecorator, FetchDecorator],
                                    builtins=type_builtins,
                                    debug=debug)

    metamodel.register_obj_processors(object_processors)

    return metamodel