import logging

import click

from yaer.runner import get_available_experiments, run_experiments

logger = logging.getLogger('yaer')


@click.group()
@click.option('--verbose', is_flag=True, help="Enable debug logging.")
@click.version_option()
def cli(verbose):
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format=fmt)
    else:
        logging.basicConfig(level=logging.INFO, format=fmt)


@click.command(name='list')
def show_available_experiments_cli():
    all_experiments = get_available_experiments()
    for e in sorted(all_experiments):
        print(e)


@click.command(name='run')
@click.option('-e', '--experiment',
              required=False,
              multiple=True,
              help=('Experiment to run. This can be specified multiple times. '
                    'See list command por options.'))
@click.option('-re', '--regular-expression',
              required=False,
              multiple=True,
              help='Run experiments that matches a regular expression')
@click.option('-d', '--dump',
              required=False,
              is_flag=True,
              help='Dump results and files.')
@click.option('--clean-previous-results',
              required=False,
              is_flag=True,
              help='Remove previous results for every runned experiment.')
@click.option('--dump_path',
              type=click.Path(),
              required=False,
              help='Base path to dump results and files.')
def run_experiments_cli(experiment, regular_expression, dump, dump_path, clean_previous_results):
    """Run listed experiments with provided datasets."""
    run_experiments(experiment, regular_expression, dump, dump_path, clean_previous_results)


cli.add_command(show_available_experiments_cli)
cli.add_command(run_experiments_cli)

if __name__ == '__main__':
    cli()
