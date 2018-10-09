import logging
import os
import shutil
from datetime import datetime

from yaer import base as runner_base
from yaer.dumpers import DumperCollection, FileDumper, LogDumper

logger = logging.getLogger('yaer')
BASE_PATH = os.path.realpath(os.curdir)


def get_experiment_info(experiment, **kwargs):
    r = {
        'experiment_name': experiment.__name__,
        'module': experiment.__module__,
        'docstring': experiment.__doc__,
        'run_datetime': datetime.strftime(datetime.utcnow(), '%c')
    }
    r.update(kwargs)
    return r


def run_experiment(experiment_name, experiment, dumper):
    """
    Runs an experiment and returns result predictor and stats.
    Predictor it's an object that must have dump and predict methods.
    """
    logger.info('Training %s', experiment_name)
    start = datetime.utcnow()
    experiment(dumper=dumper)
    stop = datetime.utcnow()
    elapsed = (stop - start).total_seconds()
    dumper.append_to_results('experiment_info', get_experiment_info(experiment,
                                                                    time_elapsed=elapsed))
    dumper.dump_results()


def get_available_experiments(experiment_pkg_path=None):
    """
    Returns a dictionary with the form <name: experiment>.
    Experiments are classes that inherits from Experiment.
    """
    if experiment_pkg_path is None:
        exp_path = os.path.join(BASE_PATH, 'experiments')

    logger.debug("About to load experiments from %s", exp_path)
    return runner_base.get_registered_experiments(exp_path)


def get_validated_experiments(included_experiments):
    validated = {}
    all_experiments = get_available_experiments()
    for e in included_experiments:
        if e not in all_experiments:
            raise ValueError('Experiment {} not exists. Available experiments: {}'.format(
                e, ', '.join(all_experiments.keys())
            ))
        validated[e] = all_experiments[e]
    return validated


def run_experiments(experiments_to_run, dump, dump_path, clean_previous_results):
    """Runs experiments based on command line parameters
    """
    validated_experiments = get_validated_experiments(experiments_to_run)
    n_experiments = len(validated_experiments)

    current_time = datetime.strftime(datetime.utcnow(), '%Y%m%d_%H%M%S')
    for i, (name, exp) in enumerate(validated_experiments.items()):
        logger.info('='*100)
        logger.info('Running %s. %s of %s experiments', name, i+1, n_experiments)
        dumpers = DumperCollection(LogDumper(name))
        if dump:
            if dump_path is None:
                dump_path = BASE_PATH
            no_time_path = os.path.join(dump_path, 'results', name)
            final_dump_path = os.path.join(no_time_path, current_time)
            if clean_previous_results and os.path.exists(no_time_path):
                logger.debug('Removing %s', no_time_path)
                shutil.rmtree(no_time_path)
            dumpers.append(FileDumper(final_dump_path))
        run_experiment(name, exp, dumpers)
        logger.info('='*100)
