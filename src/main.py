from wad.wadfile import WadReader
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--wadfile', default='wad/DOOM1.wad')
@click.option('--mapname', default='E1M1')
@click.option('--export_file', default='E1M1.jpg')
def export_map(wadfile, mapname, export_file):
    click.echo(f'Exporting {mapname} from {wadfile}')
    
    wr = WadReader(wadfile)
    
    click.echo('Done.')

if __name__ == '__main__':
    click.echo("testing")
    cli()