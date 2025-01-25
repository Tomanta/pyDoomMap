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
    limit_x, limit_y = d_map.get_limits()

    padding = 100

    img_size_x = limit_x + (padding * 2)
    img_size_y = limit_y + (padding * 2)

    out = Image.new("RGB", (img_size_x, img_size_y), (0, 0, 0))
    image = ImageDraw.Draw(out)

    for line in d_map.get_lines(use_offsets=True, padding=100):
        image.line(
            [
                line.start_vertex[0],
                img_size_y - 1 - line.start_vertex[1],
                line.end_vertex[0],
                img_size_y - 1 - line.end_vertex[1],
            ],
            fill="rgb(255,255,255)",
            width=5,
        )

    out.save(export_file)

    click.echo("Done.")


if __name__ == "__main__":
    cli()
