"""Sphinx theme for Open Free Energy software based on the PyData theme."""

# Add imports here
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.config import Config
import sass

from ._version import __version__

def html_theme_path() -> Path:
    """The path to the theme itself."""
    here = Path(__file__).parent.resolve()
    return here / "theme" / "ofe_sphinx_theme"


def compile_css(app: Sphinx, exception: Exception | None):
    """Compile SASS into CSS"""
    if exception is not None:
        return

    src = html_theme_path() / "sass/ofe-sphinx-theme.scss"
    dest = Path(app.outdir) / "_static/styles/ofe-sphinx-theme.css"

    dest.parent.mkdir(exist_ok=True, parents=True)

    css = sass.compile(
        filename=str(src),
        output_style="compressed",
    )

    print("Compiled css to bla")

    with open(dest, "w") as f:
        print(css, file=f)


def setup(app: Sphinx):
    """Set up the theme's Sphinx extension"""
    app.add_html_theme("ofe_sphinx_theme", str(html_theme_path()))

    app.connect("build-finished", compile_css)

    # usually this would be done in the `"config-init"` event,
    # but this event runs before themes are loaded
    app.config.templates_path.append(str(html_theme_path() / "templates"))

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }