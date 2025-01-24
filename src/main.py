from wad.wadfile import WadReader
from PIL import Image, ImageDraw
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("--wadfile", default="wad/DOOM1.wad")
@click.option("--mapname", default="E1M1")
@click.option("--export_file", default="export/E1M1.jpg")
def export_map(wadfile, mapname, export_file):
    click.echo(f"Exporting {mapname} from {wadfile}")
    wr = WadReader(wadfile)

    d_map = wr.maps[mapname]
    offset_x, offset_y = d_map.get_offsets()
    limit_x, limit_y = d_map.get_limits()

    padding = 100

    out = Image.new(
        "RGB", (limit_x + (padding * 2), limit_y + (padding * 2)), (0, 0, 0)
    )
    draw = ImageDraw.Draw(out)

    for linedef in d_map.linedefs:
        start_vert = d_map.vertexes[linedef.start_vertex]
        end_vert = d_map.vertexes[linedef.end_vertex]
        s = (start_vert.x + offset_x + padding, start_vert.y + offset_y + padding)
        e = (end_vert.x + offset_x + padding, end_vert.y + offset_y + padding)
        draw.line([s, e], fill="rgb(255,255,255)", width=2)

    out.save(export_file)

    click.echo("Done.")


if __name__ == "__main__":
    click.echo("testing")
    cli()
