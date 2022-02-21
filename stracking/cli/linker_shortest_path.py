import argparse
from stracking.io import read_particles, write_tracks
from stracking.linkers import SPLinker, EuclideanCost


def main():
    parser = argparse.ArgumentParser(description='STracking shortest path linker',
                                     conflict_handler='resolve')
    parser.add_argument('-i', '--input', help='input detection file', default='')
    parser.add_argument('-o', '--output', help='Output tracks file', default='')
    parser.add_argument('-f', '--format', help='output file format', default='st.json')
    parser.add_argument('-c', '--maxcost', help='Maximum connection cost', default='3000')
    parser.add_argument('-g', '--gap', help='Number of frame for gap closing ', default='1')
    args = parser.parse_args()

    particles = read_particles(args.input)
    euclidean_cost = EuclideanCost(max_cost=float(args.maxcost))
    my_tracker = SPLinker(cost=euclidean_cost, gap=int(args.gap))
    tracks = my_tracker.run(particles)
    write_tracks(args.output, tracks, format_=args.format)


if __name__ == "__main__":
    main()
