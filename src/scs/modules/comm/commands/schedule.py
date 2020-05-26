# -*- coding: utf-8 -*-
import click
import traceback
from logbook import info, warn
from flask.cli import with_appcontext
from flask import current_app

from scs import modules

async def run_task_async_each(fn, sleep):
    import trio

    while True:
        try:
            _id = fn.apply_async()
            info('append queue each {} {}'.format(fn.__name__, _id))
        except Exception as error:
            warn(error)
            warn(traceback.format_exc())

        await trio.sleep(sleep)

@click.command()
@click.pass_context
@with_appcontext
def schedule(ctx):
    """."""
    import trio

    async def run_main():
        async with trio.open_nursery() as n:
            pass

    trio.run(run_main)
