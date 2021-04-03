from __future__ import unicode_literals
import os
from os import mkdir
from os.path import exists, dirname, join
from metamodel import get_entity_mm, SimpleType
from folder_structure import create_folders, example_path
from model_instance import generate_template_and_code

def main(debug=False):
    entity_mm = get_entity_mm(debug)
    entity_model = entity_mm.model_from_file(example_path)
    create_folders()
    generate_template_and_code(entity_model)

if __name__ == "__main__":
    main()