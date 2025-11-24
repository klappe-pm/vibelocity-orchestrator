### Grok Model Operations
```bash
# List all Grok models with details
./grok.sh list
```

```bash
# Quick chat with default model
./grok.sh quick "Your prompt here"
```

```bash
# Use code-optimized model
./grok.sh code "Write a Python async web server"
```

```bash
# Use 2M context reasoning model
./grok.sh reason "Analyze this complex problem"
```

```bash
# Vision model with image
./grok.sh vision -i image.png -p "What's in this image?"
```

```bash
# Generate images
./grok.sh generate -p "A futuristic city at sunset"
```
