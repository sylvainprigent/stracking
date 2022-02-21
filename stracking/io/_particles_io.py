import numpy as np
import pandas as pd
from stracking.containers import SParticles


def read_particles(file):
    """Read particles from a file

    The CSV file must contain column with headers T, Y and X for 2D data and T, Z, Y and X for 3D
    data. All additional columns will be read as particles properties

    Parameters
    ----------
    file: str
        Path of the input file

    Returns
    -------
    SParticles container with the read file

    Raises
    ------
    IOError when the file format is not recognised or is not well formatted

    """
    reader = SParticlesIO()
    return reader.read(file)


def write_particles(file, particles):
    """Write particles into a file

    Parameters
    ----------
    file: str
        Path the file to be written
    particles: SParticles
        Particles container

    """
    writer = SParticlesIO()
    writer.write(file, particles)


class SParticlesIO:
    """Read and write particles to file"""

    def __init__(self):
        pass

    @staticmethod
    def read(file):
        if file.endswith('.csv') or file.endswith('.CSV'):
            return CSVParticlesIO.read_csv_particles(file)
        else:
            raise IOError(f'SParticlesIO can read only CSV files')

    @staticmethod
    def write(file, particles):
        if file.endswith('.csv') or file.endswith('.CSV'):
            return CSVParticlesIO.write_csv_particles(file, particles)
        else:
            raise IOError(f'SParticlesIO can read only CSV files')


class CSVParticlesIO:
    """Read and Write particles from CSV files

    The CSV file must contain column with headers T, Y and X for 2D data and T, Z, Y and X for 3D
    data. All additional columns will be read as particles properties

    """
    def __init__(self):
        pass

    @staticmethod
    def _read_properties(df):
        properties = {}
        header = df.columns.values.tolist()
        for h in header:
            if h != 'T' and h != 'Z' and h != 'Y' and h != 'X':
                properties[h] = df[h].values
        return properties

    @staticmethod
    def read_csv_particles(file):
        df = pd.read_csv(file)
        header = df.columns.values.tolist()
        if 'T' in header and 'X' in header and 'Y' in header and 'Z' not in header:  # 2D+t
            particles = SParticles()
            data = np.zeros((df.shape[0], 3))
            for index, row in df.iterrows():
                data[index, 0] = row['T']
                data[index, 1] = row['Y']
                data[index, 2] = row['X']
            particles.data = data
            particles.properties = CSVParticlesIO._read_properties(df)
            return particles
        elif 'T' in header and 'X' in header and 'Y' in header and 'Z' in header:  # 3D+t
            particles = SParticles()
            data = np.zeros((df.shape[0], 4))
            for index, row in df.iterrows():
                data[index, 0] = row['T']
                data[index, 1] = row['Z']
                data[index, 2] = row['Y']
                data[index, 3] = row['X']
            particles.data = data
            particles.properties = CSVParticlesIO._read_properties(df)
            return particles
        else:
            raise IOError('A CSV particle file must have T, Y, X columns')

    @staticmethod
    def write_csv_particles(file, particles):
        if particles.data.shape[1] == 3:  # 2D+t
            data_mat = particles.data.copy()
            columns = ['T', 'Y', 'X']
            for prop, values in particles.properties.items():
                columns.append(prop)
                data_mat = np.column_stack((data_mat, values))
            df = pd.DataFrame(data_mat, columns=columns)
            df.to_csv(file, index=False)
        else:
            data_mat = particles.data.copy()
            columns = ['T', 'Z', 'Y', 'X']
            for prop, values in particles.properties.items():
                columns.append(prop)
                data_mat = np.column_stack((data_mat, values))
            df = pd.DataFrame(data_mat, columns=columns)
            df.to_csv(file, index=False)
