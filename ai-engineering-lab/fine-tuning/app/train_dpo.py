import json
import os
from pathlib import Path

from peft import AutoPeftModelForCausalLM
from trl import DPOConfig, DPOTrainer

from app.data import preference_dataset


def main() -> None:
    sft_adapter = os.getenv("SFT_ADAPTER", "artifacts/sft-lora")
    output_dir = os.getenv("DPO_OUTPUT_DIR", "artifacts/dpo-lora")
    rows = json.loads(Path("data/preferences.json").read_text(encoding="utf-8"))
    dataset = preference_dataset(rows)

    model = AutoPeftModelForCausalLM.from_pretrained(sft_adapter, is_trainable=True)
    config = DPOConfig(
        output_dir=output_dir,
        learning_rate=5e-5,
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        logging_steps=10,
        save_strategy="epoch",
        report_to="none",
    )
    trainer = DPOTrainer(
        model=model,
        args=config,
        train_dataset=dataset,
    )
    trainer.train()
    trainer.save_model(output_dir)


if __name__ == "__main__":
    main()
