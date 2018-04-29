import inspect
from importlib.util import module_from_spec, spec_from_file_location
import os

from yaer.dumpers import LogDumper


_loaded = False
_registered_experiments = {}


def _load_experiment_modules(exp_path):
    for dirpath, _, filenames in os.walk(exp_path):
        for filename in filenames:
            if not filename.startswith('__') and filename.endswith(".py"):
                path = os.path.join(dirpath, filename)
                module = path.replace(os.path.sep, '.')[:-3]
                spec = spec_from_file_location(module, path)
                module = module_from_spec(spec)
                spec.loader.exec_module(module)


def get_registered_experiments(exp_path):
    global _loaded
    if not _loaded:
        _load_experiment_modules(exp_path)
        _loaded = True

    return _registered_experiments


_current_context = None


def experiment(configs=None):
    if configs is None:
        configs = {}

    def inner(f):
        def the_experiment(*args, **kwargs):
            global _current_context
            configs['dumper'] = kwargs.get('dumper', LogDumper(f.__name__))
            _current_context = configs
            new_params = get_updated_params(f, configs, args, kwargs)
            f(**new_params)
            _current_context = None

        the_experiment.__name__ = f.__name__
        the_experiment.__module__ = f.__module__
        the_experiment.__doc__ = f.__doc__
        _registered_experiments[f.__name__] = the_experiment
        return the_experiment
    return inner


def experiment_component(f):
    global _current_context

    def inner(*args, **kwargs):
        if _current_context is not None:
            _current_context.dumper.append_to_results('{}_info'.format(f.__name__),
                                                      {'docstring': f.__doc__,
                                                       'module': f.__module__})
            new_params = get_updated_params(f, _current_context, args, kwargs)
            return f(**new_params)
        else:
            return f(*args, **kwargs)
    return inner


def get_updated_params(f, configs, args, kwargs):
    args_names = inspect.getargs(f.__code__).args
    current_args = dict(zip(args_names, args))
    current_args.update(kwargs)
    full_replacement = {k: v for k, v in configs.items() if k in args_names}
    full_replacement.update(current_args)
    return full_replacement
