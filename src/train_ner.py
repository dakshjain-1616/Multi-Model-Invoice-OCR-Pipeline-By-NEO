import json
import torch
import numpy as np
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer, DataCollatorForTokenClassification
import evaluate

# 1. Load data
with open("data/dataset.json", "r") as f:
    raw_data = json.load(f)

label_list = ["O", "B-VENDOR", "B-DATE", "B-ITEM", "B-TOTAL"]
label_to_id = {l: i for i, l in enumerate(label_list)}

def prepare_ner_data(raw_data):
    formatted_data = []
    for entry in raw_data:
        # For simplicity in this synthetic task, we treat each entity as a sequence of tokens
        # In a real scenario, we'd tokenize the whole document text.
        # Here we create a simple sentence for each invoice.
        tokens = []
        labels = []
        for ent in entry['entities']:
            word_tokens = ent['text'].split()
            for i, word in enumerate(word_tokens):
                tokens.append(word)
                labels.append(label_to_id[ent['label']]) # Simplification: all words in entity get the tag
        formatted_data.append({"tokens": tokens, "ner_tags": labels})
    return formatted_data

data = prepare_ner_data(raw_data)
dataset = Dataset.from_list(data)
dataset = dataset.train_test_split(test_size=0.2)

# 2. Tokenization
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples[f"ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            else:
                label_ids.append(label[word_idx])
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=True)

# 3. Model
model = AutoModelForTokenClassification.from_pretrained(
    "bert-base-multilingual-cased", num_labels=len(label_list)
)

# 4. Metrics
seqeval = evaluate.load("seqeval")

def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)
    
    true_predictions = []
    true_labels = []
    
    for prediction, label in zip(predictions, labels):
        p_list = []
        l_list = []
        for p_id, l_id in zip(prediction, label):
            if l_id != -100:
                p_list.append(label_list[p_id])
                l_list.append(label_list[l_id])
        if p_list: # Ensure non-empty lists
            true_predictions.append(p_list)
            true_labels.append(l_list)
            
    results = seqeval.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

# 5. Training
training_args = TrainingArguments(
output_dir="./results",
eval_strategy="epoch",  # Fixed argument name for newer versions
learning_rate=2e-5,
per_device_train_batch_size=8,
num_train_epochs=3,
weight_decay=0.01,
use_cpu=True,
logging_steps=10
)

trainer = Trainer(
model=model,
args=training_args,
train_dataset=tokenized_datasets["train"],
eval_dataset=tokenized_datasets["test"],
processing_class=tokenizer,
data_collator=DataCollatorForTokenClassification(tokenizer),
compute_metrics=compute_metrics,
)

print("Starting CPU fine-tuning...")
trainer.train()
trainer.save_model("./model/invoice_ner_bert")
print("Model saved to ./model/invoice_ner_bert")