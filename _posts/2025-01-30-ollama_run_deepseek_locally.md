---
image: https://mylemans.online/assets/img/posts/Default.jpg
layout: post
title: "How to Install Ollama on Windows and Run DeepSeek R1 Locally"
date: 2025-01-30
categories: [AI, Windows, Machine Learning]
tags: [Ollama, AI, LLM, Windows, Machine Learning, DeepSeek R1, Open-Source AI]
description: "Learn how to install Ollama on Windows and run DeepSeek R1, Llama 2, and other AI models locally. A step-by-step guide for setting up open-source LLMs without cloud dependency."
---

{% include google-adsense.html %}

## How to Install Ollama on Windows and Run DeepSeek R1 Locally  

Running **large language models (LLMs) locally** has never been easier. With **Ollama**, you can install and use **DeepSeek R1, Llama 2, Gemma, and more** right on your Windows machine—no cloud computing required.  

In this guide, you'll learn:  
- How to **install Ollama on Windows**  
- How to **run DeepSeek R1**, the trending **67B parameter AI model**  
- How to use other models like **Llama 2 and Gemma** locally  

Let’s get started.  

### Step 1: Download and Install Ollama  

Installing Ollama is straightforward—just follow these steps:  

1. Head over to the official **[Ollama download page](https://ollama.com/download)**.  
2. Click on the **Windows download** option.  
3. Once the installer is downloaded, **run the setup file**.  
4. Follow the installation prompts (it’s a simple “Next, Next, Finish” process).  
5. Once installed, you’re ready to start using AI models on your local machine.  

### Step 2: Open the Command Line  

Ollama runs from the **command line (CMD or PowerShell)**. If you’ve never used the command line before, don’t worry—it’s easier than it looks.  

- Open the **Command Prompt** by pressing `Win + R`, typing `cmd`, and hitting **Enter**.  
- Alternatively, you can use **PowerShell** (just search for it in the Start Menu).  

### Step 3: Run Your First AI Model  

Now for the fun part. Ollama allows you to run AI models with a simple command. Let’s start with **Llama 2**, a powerful open-source language model:  

```sh
ollama run llama2
```

When you run this command:

Ollama will automatically download the Llama 2 model if you don’t already have it.
Once downloaded, it will start running the AI model, and you can chat with it right from the command line.


### Step 4: Running DeepSeek R1 Locally
What is DeepSeek R1?
DeepSeek R1 is a 67B parameter, open-weight LLM, optimized for reasoning and complex AI tasks. It is one of the most powerful open-source alternatives to GPT-4, making it highly sought after by AI researchers and developers.

How to Install and Run DeepSeek R1
To run DeepSeek R1 on your local machine using Ollama, enter:

```sh
ollama run deepseek-r1
```

If this is your first time running DeepSeek R1, Ollama will automatically download the model before starting the session.

### DeepSeek R1 vs. Llama 2  

DeepSeek R1 and Llama 2 are both powerful open-source language models, but they have different strengths. Here’s a comparison:  

| Feature         | DeepSeek R1 | Llama 2 |
|---------------|------------|---------|
| Model Size    | 67B        | 7B / 13B / 65B |
| Reasoning Ability | Advanced | Moderate |
| Open-Weight   | ✅ Yes      | ✅ Yes |
| Ideal For     | Complex AI tasks, coding, research | General-purpose AI |

DeepSeek R1 excels in **reasoning, problem-solving, and handling complex queries**, making it a great alternative to closed-source models like GPT-4.  

### Step 5: Explore Other AI Models  

Ollama supports many open-source models. To see the full list, run:  

```sh
ollama list
```

To run any model, use:

```sh
ollama run <model-name>
```

For example, to run Gemma, type:

```sh
ollama run gemma
```

## Why Use Ollama for Local AI Models?

Running DeepSeek R1, Llama 2, and other AI models locally with Ollama has several advantages:

- No cloud dependency – Run models without an internet connection.
- Full control over AI – No third-party monitoring or restrictions.
- Lower costs – Avoid cloud-based API fees.
- Faster response times – No latency issues from remote servers.

## Conclusion
By installing Ollama on Windows, you can run DeepSeek R1, Llama 2, and other LLMs entirely on your own hardware. This setup is ideal for developers, AI enthusiasts, and researchers looking to leverage powerful AI without relying on cloud services.

For more details, check out the official [Ollama documentation](https://ollama.com/).
