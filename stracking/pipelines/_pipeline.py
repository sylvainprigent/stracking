import os
import json

from stracking import detectors
from stracking import linkers
from stracking import properties
from stracking import features
from stracking import filters


class STrackingPipeline:
    def __init__(self):
        self.name = ''
        self.date = ''
        self.author = ''
        self.stracking_version = ''
        self._detector = None
        self._linker = None
        self._properties = []
        self._features = []
        self._filters = []

    @staticmethod
    def _read_json(file_path: str):
        """Read the metadata from the a json file"""
        if os.path.getsize(file_path) > 0:
            with open(file_path) as json_file:
                return json.load(json_file)

    @staticmethod
    def _write_json(metadata: dict, file_path: str):
        """Write the metadata to the a json file"""
        with open(file_path, 'w') as outfile:
            json.dump(metadata, outfile, indent=2)

    def load(self, file):
        """Load the pipeline from a json file

        Parameters
        ----------
        file: str
            Path of the pipeline json file

        """
        json_data = self._read_json(file)
        if 'name' in json_data:
            self.name = json_data['name']
        if 'date' in json_data:
            self.date = json_data['date']
        if 'author' in json_data:
            self.author = json_data['author']
        if 'stracking_version' in json_data:
            self.stracking_version = json_data['stracking_version']
        if 'detector' in json_data['steps']:
            if 'name' in json_data['steps']['detector']:
                parameters = {}
                if 'parameters' in json_data['steps']['detector']:
                    parameters = json_data['steps']['detector']['parameters']
                print('load the detector:', json_data['steps']['detector']['name'])
                self._detector = getattr(detectors, json_data['steps']['detector']['name'])(**parameters)
        if 'linker' in json_data['steps']:
            if 'name' in json_data['steps']['linker']:
                cost_fn = None
                if 'cost' in json_data['steps']['linker']:
                    cost_params = json_data['steps']['linker']['cost']['parameters']
                    cost_fn = getattr(linkers, json_data['steps']['linker']['cost']['name'])(**cost_params)
                parameters = {}
                if 'parameters' in json_data['steps']['linker']:
                    parameters = json_data['steps']['linker']['parameters']
                self._linker = getattr(linkers, json_data['steps']['linker']['name'])(cost_fn, **parameters)
        if 'properties' in json_data['steps']:
            for prop in json_data['steps']['properties']:
                params = {}
                if "parameters" in prop:
                    params = prop["parameters"]
                self._properties.append(getattr(properties, prop['name'])(**params))
        if 'features' in json_data['steps']:
            for feat in json_data['steps']["features"]:
                params = {}
                if "parameters" in feat:
                    params = feat["parameters"]
                self._features.append(getattr(features, feat['name'])(**params))
        if 'filters' in json_data['steps']:
            for filter_ in json_data['steps']['filters']:
                params = {}
                if "parameters" in filter_:
                    params = filter_["parameters"]
                self._filters.append(getattr(filters, filter_['name'])(**params))

    def run(self, image):
        """Run the pipeline on an image

        Parameters
        ----------
        image: ndarray

        Returns
        -------
        A STracks container of the extracted tracks

        """
        particles = self._detector.run(image)
        for prop in self._properties:
            particles = prop.run(particles, image)
        print('particles:', particles.data)
        print('particles properties:', particles.properties)
        tracks = self._linker.run(particles, image)
        for feat in self._features:
            tracks = feat.run(tracks)

        print('tracks:', tracks.data)
        print('tracks properties:', tracks.properties)
        print('tracks features:', tracks.features)
        #tracks = match_properties(particles, tracks)
        #print('tracks properties:', tracks.properties)
        #print('tracks features:', tracks.features)

        for filter_ in self._filters:
            tracks = filter_.run(tracks)
        print('tracks out:', tracks.data)
        print('tracks properties out:', tracks.properties)
        print('tracks features out:', tracks.features)
        return tracks
