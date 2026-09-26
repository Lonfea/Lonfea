import json
import os
from pathlib import Path

from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

from app.data import sft_dataset


def main() -> None:
    model_id = os.getenv("BASE_MODEL", "Qwen/Qwen3-0.6B")
    output_dir = os.getenv("OUTPUT_DIR", "artifacts/sft-lora")
    rows = json.loads(Path("data/sft.json").read_text(encoding="utf-8"))
    dataset = sft_dataset(rows)

    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    config = SFTConfig(
        output_dir=output_dir,
        learning_rate=1e-4,
        num_train_epochs=1,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        completion_only_loss=True,
        logging_steps=10,
        save_strategy="epoch",
        report_to="none",
    )
    trainer = SFTTrainer(
        model=model_id,
        args=config,
        train_dataset=dataset,
        peft_config=peft_config,
    )
    trainer.train()
    trainer.save_model(output_dir)


if __name__ == "__main__":
    main()
