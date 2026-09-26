from datasets import Dataset


def validate_sft_rows(rows: list[dict]) -> None:
    for index, row in enumerate(rows):
        if not isinstance(row.get("prompt"), str) or not row["prompt"].strip():
            raise ValueError(f"SFT row {index} is missing a prompt.")
        if not isinstance(row.get("completion"), str) or not row["completion"].strip():
            raise ValueError(f"SFT row {index} is missing a completion.")


def validate_preference_rows(rows: list[dict]) -> None:
    for index, row in enumerate(rows):
        required = ("prompt", "chosen", "rejected")
        if any(not isinstance(row.get(key), str) or not row[key].strip() for key in required):
            raise ValueError(f"Preference row {index} must contain prompt/chosen/rejected.")
        if row["chosen"] == row["rejected"]:
            raise ValueError(f"Preference row {index} has identical chosen and rejected answers.")


def sft_dataset(rows: list[dict]) -> Dataset:
    validate_sft_rows(rows)
    return Dataset.from_list(rows)


def preference_dataset(rows: list[dict]) -> Dataset:
    validate_preference_rows(rows)
    return Dataset.from_list(rows)
