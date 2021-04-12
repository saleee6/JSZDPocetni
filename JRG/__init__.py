import os
from JRG.python_files.metamodel import get_entity_mm
from JRG.python_files.folder_structure import create_folders
from JRG.python_files.model_instance import generate_template_and_code
from textx import language, generator
import click

@language('full_stack_lang', '*.jrg')
def full_stack_lang():
    ''' Language description '''
    return get_entity_mm()

@generator('full_stack_lang', 'fullstack')
def full_stack_gen(metamodel, model, output_path, overwrite, debug):
    ''' Generator description '''
    input_file = model._tx_filename
    base_dir = output_path if output_path else os.path.dirname(input_file)
    base_name, _ = os.path.splitext(os.path.basename(input_file))
    output_folder = os.path.abspath(os.path.join(base_dir, base_name))

    if overwrite or not os.path.exists(output_folder):
        click.echo('-> {}'.format(output_folder))
        create_folders(base_dir, base_name)
        generate_template_and_code(model)
        click.echo('Success')
    else:
        click.echo('-- Skipping: {}'.format(output_folder))