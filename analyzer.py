# -*- coding: utf-8 -*-
from __future__ import print_function, division
import sys
import os
from arch import compute_routing_usage
from arch import parse_routing
from arch import compute_total_wire
from arch import parse_placement, parse_cgra, compute_area_usage
from arch.cgra_route import parse_routing_resource, build_routing_resource


def main():
    if len(sys.argv) != 4:
        print("Usage:", sys.argv[0], "<cgra_info.txt>", "<netlist.json>",
              "<netlist.route>",
              file=sys.stderr)
        exit(1)
    cgra_file = sys.argv[1]
    netlist = sys.argv[2]
    route_file = sys.argv[3]
    packed_file = route_file.replace(".route", ".packed")
    placement_file = route_file.replace(".route", ".place")
    board_layout = parse_cgra(cgra_file)["CGRA"]
    routing_result = parse_routing(route_file)
    placement, _ = parse_placement(placement_file)

    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        meta = os.popen('stty size', 'r').read().split()
        cols = int(meta[-1])
        cols = int(cols)
        scale = cols - 15
    else:
        scale = 68
        cols = 80

    print("-" * cols)
    print("Area Usage:")
    usage = compute_area_usage(placement, board_layout)
    for entry in usage:
        percentage = usage[entry][0] / usage[entry][1] * 100
        num_bar = max(int(percentage / 100 * scale) - 2, 1)
        print("{0:4s} {1} {2} {3:.2f}%".format(entry.upper(),
                                               num_bar * '█',
                                               ' ' * (scale - num_bar - 2),
                                               percentage))

    print("-" * cols)
    net_wire = compute_total_wire(routing_result)
    total_wire = sum([net_wire[x] for x in net_wire])
    print("Total wire:", total_wire)

    # timing removed for future development

    print("-" * cols)
    r = parse_routing_resource(cgra_file)
    routing_resource = build_routing_resource(r)
    resource_usage = compute_routing_usage(routing_result, routing_resource)
    for bus in resource_usage:
        print("BUS:", bus)
        for track in resource_usage[bus]:
            total, left = resource_usage[bus][track]
            percentage = (total - left) / total * 100
            num_bar = int(percentage / 100 * scale)
            print("TRACK {0} {1} {2} {3:.2f}%".format(track,
                                                      num_bar * '█',
                                                      ' ' * (scale -
                                                             num_bar - 5),
                                                      percentage))


if __name__ == '__main__':
    main()
