import click

from .server import generate_authenticated_server

@click.group()
def main() -> None:
    pass

@main.command()
@click.option(
    "--print-routes",
    required=False,
    default=False,
    is_flag=True,
    help="List all the generated routes",
)
@click.option("--port", default=5050, type=int, help="Port to host application on")
@click.option("--public-key", "-k", type=str, help="Public key for decoding JWTs")
@click.option("--issuer", "-i", type=str, help="JWT issuer to validate JWTs for")
@click.option(
    "--cors/--no-cors",
    is_flag=True,
    default=True,
    help="Specify whether CORS should be allowed",
)
def server(print_routes: bool, port: int, public_key: str, issuer: str, cors: bool) -> None:
    """Run the authenticated HPI_API server"""
    app: Flask = generate_authenticated_server(cors=cors, public_key=public_key, issuer=issuer)
    if print_routes:
        for rule in app.url_map.iter_rules():
            click.echo(str(rule))
    else:
        app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
