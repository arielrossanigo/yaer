from abc import ABC, abstractmethod
import json
import os
import pickle
import logging
import pandas as pd


class BaseDumper(ABC):
    def __init__(self):
        self.results = {}

    def append_to_results(self, key, value):
        self.results[key] = value

    @abstractmethod
    def dump_binarie(self, filename, obj):
        raise NotImplementedError

    @abstractmethod
    def dump_results(self):
        raise NotImplementedError

    @abstractmethod
    def dump_json(self, filename, obj):
        raise NotImplementedError

    @abstractmethod
    def dump_csv(self, filename, obj):
        raise NotImplementedError


class DumperCollection(BaseDumper):
    def __init__(self, *dumpers):
        self.dumpers = list(dumpers)

    def append(self, dumper):
        self.dumpers.append(dumper)

    def append_to_results(self, key, value):
        for dumper in self.dumpers:
            dumper.append_to_results(key, value)

    def dump_binarie(self, filename, obj):
        for dumper in self.dumpers:
            dumper.dump_binarie(filename, obj)

    def dump_results(self):
        for dumper in self.dumpers:
            dumper.dump_results()

    def dump_json(self, filename, obj):
        for dumper in self.dumpers:
            dumper.dump_json(filename, obj)

    def dump_csv(self, filename, obj):
        for dumper in self.dumpers:
            dumper.dump_csv(filename, obj)


class LogDumper(BaseDumper):
    def __init__(self, loggername):
        super().__init__()
        self.logger = logging.getLogger(loggername)

    def dump_binarie(self, filename, obj):
        self.logger.info("Dump binarie file %s", filename)

    def dump_results(self):
        self.logger.info("Dumped results.\n%s", json.dumps(self.results, indent=4, sort_keys=True))

    def dump_json(self, filename, obj):
        self.logger.info("Dumped json.\n%s", json.dumps(obj, indent=4, sort_keys=True))

    def dump_csv(self, filename, obj):
        self.logger.info("Dumped csv.\n%s", filename)


class FileDumper(BaseDumper):
    def __init__(self, path):
        super().__init__()
        os.makedirs(path)
        self.path = path

    def dump_binarie(self, filename, obj):
        with open(os.path.join(self.path, filename), 'wb') as f:
            pickle.dump(obj, f)

    def dump_results(self):
        with open(os.path.join(self.path, 'results.json'), 'wt') as f:
            json.dump(self.results, f, indent=4, sort_keys=True)

    def dump_json(self, filename, obj):
        with open(os.path.join(self.path, filename), 'wt') as f:
            json.dump(obj, f)

    def dump_csv(self, filename, obj):
        if type(obj) in (pd.Series, pd.DataFrame):
            obj.to_csv(os.path.join(self.path, filename))
        else:
            raise Exception("DataFrame or Series expected.")
