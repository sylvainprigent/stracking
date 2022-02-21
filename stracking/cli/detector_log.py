import os
import argparse
from skimage.io import imread
from stracking.detectors import LoGDetector
from stracking.io import write_particles


def main():
    parser = argparse.ArgumentParser(description='STracking LoG detector',
                                     conflict_handler='resolve')
    parser.add_argument('-i', '--input', help='input image file', default='')
    parser.add_argument('-o', '--output', help='Output image file', default='')
    parser.add_argument('-a', '--minsigma', help='Minimum sigma value', default='4')
    parser.add_argument('-b', '--maxsigma', help='Maximum sigma value', default='5')
    parser.add_argument('-n', '--numsigma', help='Number of sigma value', default='10')
    parser.add_argument('-t', '--threshold', help='Detection threshold', default='0.2')
    parser.add_argument('-l', '--overlap', help='Allowed detection overlap fraction in [0, 1]',
                        default='0.5')
    args = parser.parse_args()

    if os.path.exists(args.input):
        image = imread(args.input)
    else:
        print('ERROR: The input image file does not exists')
        return
    detector = LoGDetector(min_sigma=float(args.minsigma),
                           max_sigma=float(args.maxsigma),
                           num_sigma=int(args.numsigma),
                           threshold=float(args.threshold),
                           overlap=float(args.overlap))
    particles = detector.run(image)
    write_particles(args.output, particles)


if __name__ == "__main__":
    main()
