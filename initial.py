from __future__ import unicode_literals
import os
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from datetime import datetime

this_folder = dirname(__file__)
grammar_path = join(this_folder, 'grammar.tx')
template_folder = join(this_folder, 'templates')

class SimpleType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name

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

    metamodel = metamodel_from_file(grammar_path,
                                    classes=[SimpleType],
                                    builtins=type_builtins,
                                    debug=debug)

    return metamodel

def main(debug=False):

    entity_mm = get_entity_mm(debug)

    def javatype(s):
        """
        Maps type names from SimpleType to Java.
        """
        return {
                'string': 'String'
        }.get(s.name, s.name)

    def isSimpleType(s):
        """
        Check property type.
        """
        return isinstance(s, SimpleType)

    # Create the output folder
    srcgen_folder = join(this_folder, 'generated')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    # Initialize the template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register the filter for mapping Entity type names to Java type names.
    jinja_env.filters['javatype'] = javatype
    jinja_env.filters['isSimpleType'] = isSimpleType

    # Load the Java template
    template = jinja_env.get_template('entity.template')

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
    for entity in entity_model.entities:
        # For each entity generate java file
        with open(join(srcgen_folder,
                      "%s.java" % entity.name.capitalize()), 'w') as f:
            f.write(template.render(entity=entity, time=dt_string))


if __name__ == "__main__":
    main()