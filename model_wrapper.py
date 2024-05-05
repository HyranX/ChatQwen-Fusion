# model_wrapper.py
## testing vscode

def call_chatglm(tokenizer, model, prompt, history):
    response, history = model.chat(tokenizer, prompt, history=history)
    return response, history

def call_qwen(tokenizer, model, prompt, device):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def generate_response(tokenizer, model, prompt, history=None, model_type='chatglm', device=None):
    if model_type == 'chatglm':
        return call_chatglm(tokenizer, model, prompt, history)
    elif model_type == 'qwen':
        if device is None:
            raise ValueError("Device must be specified for Qwen model.")
        return call_qwen(tokenizer, model, prompt, device), history
    else:
        raise ValueError("Invalid model type specified.")
