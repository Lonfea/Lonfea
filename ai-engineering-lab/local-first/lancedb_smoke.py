from pathlib import Path

import lancedb
import pyarrow as pa


def main() -> None:
    root = Path(".local/lancedb")
    root.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(root)

    schema = pa.schema(
        [
            pa.field("id", pa.int64()),
            pa.field("text", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), 3)),
        ]
    )
    rows = [
        {"id": 1, "text": "climate risk", "vector": [1.0, 0.0, 0.0]},
        {"id": 2, "text": "business analytics", "vector": [0.0, 1.0, 0.0]},
    ]
    table = db.create_table("smoke", data=rows, schema=schema, mode="overwrite")
    result = table.search([1.0, 0.0, 0.0]).limit(1).to_list()
    assert result[0]["id"] == 1
    print("LanceDB local vector smoke test passed.")


if __name__ == "__main__":
    main()
