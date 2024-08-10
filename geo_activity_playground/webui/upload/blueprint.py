from flask import Blueprint
from flask import render_template

from ...core.activities import ActivityRepository
from ...explorer.tile_visits import TileVisitAccessor
from .controller import UploadController
from geo_activity_playground.core.config import Config


def make_upload_blueprint(
    repository: ActivityRepository,
    tile_visit_accessor: TileVisitAccessor,
    old_config: dict,
    config: Config,
) -> Blueprint:
    blueprint = Blueprint("upload", __name__, template_folder="templates")

    upload_controller = UploadController(
        repository, tile_visit_accessor, old_config, config
    )

    @blueprint.route("/")
    def index():
        return render_template(
            "upload/index.html.j2", **upload_controller.render_form()
        )

    @blueprint.route("/receive", methods=["POST"])
    def receive():
        return upload_controller.receive()

    return blueprint
