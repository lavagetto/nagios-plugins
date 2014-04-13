#!/usr/bin/env python
"""
check_graphite.py
~~~~~~~

:copyright: (c) 2014 Wikimedia Foundation
:license: Apache License 2.0, see LICENSE for more details.
"""

import os
import json
from urllib import urlencode
import urllib2
from numbers import Real
import argparse


class GraphiteCheck(object):
    pass

class Threshold(GraphiteCheck):
    pass

class Anomaly(GraphiteCheck):
    pass

def main():
    """
    Controller for the graphite fetching plugin.

    You can build a few different type of checks, both traditional nagios checks and anomaly detection ones.

    Examples:

    Check if a metric exceeds a certain value 10 times in the last 20 minutes:

    ./check_graphyte.py --url http://some-graphite-host  -C 10 -W 5 check_threshold my.beloved.metric  --from -20m --threshold 100 --over

    Check if a metric has exceeded its holter-winters confidence bands 5% of the times over the last 500 checks

    ./check_graphyte.py --url http://some-graphite-host -C 5 -W 1 check_anomaly my.beloved.metric  --check_window 500

    """
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(
        title='check_type',
        help='use with --help for additional help',
        dest='check_type')

    threshold = subparsers.add_parser(
        'check_threshold',
        help='Checks if the metric exceeds the desired threshold')
    threshold.add_argument('metric', metavar='METRIC', help='the metric to fetch from graphite')
    threshold.add_argument('--over', dest="over", action='store_true', default=True, help='If alarms should happen when we exceed the threshold')
    threshold.add_argument('--under', dest="under", action='store_true', default=False, help='If alarms should happen when we are below the threshold')
    threshold.set_defaults(cls=Threshold)

    anomaly = subparsers.add_parser(
        'check_anomaly',
        help='Checks if the metric is out of the forecasted bounds for a number of times in the last iterations')
    anomaly.add_argument('metric', metavar='METRIC', help='the metric to fetch from graphite')
    anomaly.add_argument('--check_window', dest="check_window", type=int, help='How many datapoints to consider in the anomaly detection')
    anomaly.set_defaults(cls=Anomaly)

    parser.add_argument('-U', '--url', dest='url',
                        default=os.environ.get('GRAPHITE_URL', 'http://localhost'),
                        help='Url of the graphite server'
                        )
    parser.add_argument('-C', '--critical', dest='crit', type=int, help='Threshold for critical alert (integer)')
    parser.add_argument('-W', '--warning', dest='warn', type=int, help='Threshold for warning (integer)')

    args = parser.parse_args()
    #action = cls(metric)
#    action->fetch_data()
    print(args)


if __name__ == '__main__':
    main()
