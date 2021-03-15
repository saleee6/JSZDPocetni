from __future__ import unicode_literals
import os
from os.path import dirname, join
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

this_folder = dirname(__file__)
grammar_path = join(this_folder, 'grammar.tx')

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

    # Export to .dot file for visualization
    dot_folder = join(this_folder, 'dotexport')
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)
    metamodel_export(entity_mm, join(dot_folder, 'grammar_meta.dot'))

    # Izgradnja modela u odnosu na konkretan primer
    example_model = entity_mm.model_from_file(join(this_folder, 'example.jszd'))

    print(example_model.entities)

    # Kreiranje .dot fajla u odnosu na izgradjeni model
    model_export(example_model, join(dot_folder, 'example.dot'))


if __name__ == "__main__":
    main()