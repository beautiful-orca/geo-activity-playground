import hashlib
import logging
import pathlib

import pandas as pd

from geo_activity_playground.core.activity_parsers import read_activity

logger = logging.getLogger(__name__)


def import_from_directory() -> None:
    meta_file = pathlib.Path("Cache") / "activities.parquet"
    if meta_file.exists():
        logger.info("Loading metadata file …")
        meta = pd.read_parquet(meta_file)
    else:
        logger.info("Didn't find a metadata file.")
        meta = None

    already_parsed = set(meta.id) if meta is not None else set()

    activity_stream_dir = pathlib.Path("Cache/Activity Timeseries")
    new_rows: list[dict] = []
    for path in pathlib.Path("Activities").rglob("*.*"):
        id = int(hashlib.sha3_224(str(path).encode()).hexdigest(), 16) % 2**62
        if id in already_parsed:
            continue

        logger.info(f"Parsing activity file {path} …")
        timeseries = read_activity(path)
        timeseries_path = pathlib.Path(f"Cache/Activity Timeseries/{id}.parquet")
        timeseries_path.parent.mkdir(exist_ok=True, parents=True)
        timeseries.to_pickle(timeseries_path)
        new_rows.append(
            {
                "id": id,
                "commute": None,
                "distance": 0,
                "name": path.stem,
                "kind": None,
                "start": timeseries["time"].iloc[0],
                "elapsed_time": timeseries["time"].iloc[-1]
                - timeseries["time"].iloc[0],
                "equipment": None,
                "calories": 0,
            }
        )

    new_df = pd.DataFrame(new_rows)
    merged: pd.DataFrame = pd.concat([meta, new_df])
    merged.sort_values("start", inplace=True)
    meta_file.parent.mkdir(exist_ok=True, parents=True)
    merged.to_parquet(meta_file)
