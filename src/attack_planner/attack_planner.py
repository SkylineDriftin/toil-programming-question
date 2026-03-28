#!/usr/bin/env python3

import click
import json
import sys
from src.attack_planner.distribution_network import DistributionNetwork

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def cli(input_filepath, output_filepath):
    try:
        # first lets load the distribution network from the json filepath provided
        network_data = open_json(input_filepath)
        # lets make a distribution network to check
        distribution_network = DistributionNetwork.from_json(network_data)
        # now run attack
        attack_plan = distribution_network.plan_attack()
        # now lets store the json
        store_json(output_filepath, attack_plan)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def store_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def open_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    cli()