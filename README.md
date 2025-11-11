# AI Agent - Local ChatGPT/Gemini Alternative

A beautiful, local AI chat agent powered by Google Gemini API. Perfect for when ChatGPT or Gemini websites are blocked on your network. This application runs entirely on your local machine and communicates directly with the Gemini API.

## Features

- 🤖 **Powered by Google Gemini** - Uses the latest Gemini 1.5 Flash model
- 💬 **ChatGPT-like Interface** - Beautiful, modern chat UI
- 📝 **Markdown Support** - Renders code blocks, lists, headers, and more
- 🔄 **Conversation History** - Maintains context throughout the conversation
- 🎨 **Modern Design** - Clean, responsive interface
- 🚀 **Fast & Lightweight** - Built with FastAPI and vanilla JavaScript
- 🔒 **Local Only** - Runs entirely on your machine
- 🧹 **Clear Conversation** - Reset chat history with one click

## Prerequisites

- Python 3.8 or higher
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   - Copy `env.example` to `.env`:
     ```bash
     # On Windows (PowerShell):
     Copy-Item env.example .env
     
     # On Linux/Mac:
     cp env.example .env
     ```
   - Open `.env` and add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

## Usage

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   - Navigate to `http://localhost:8000`
   - The chat interface will load automatically

3. **Start chatting!**
   - Type your message and press Enter or click Send
   - The AI will respond using the Gemini API
   - Use the "Clear" button to reset the conversation

## Configuration

### Change the Model

You can switch between different Gemini models in `app.py`:

- `gemini-1.5-flash` (default) - Fast and efficient, good for most use cases
- `gemini-1.5-pro` - Better quality, slower response time

Edit line 42 in `app.py`:
```python
model = genai.GenerativeModel('gemini-1.5-pro')  # Change to 'gemini-1.5-pro' for better quality
```

### Change the Port

Set the `PORT` environment variable in your `.env` file:
```
PORT=8080
```

Or modify line 131 in `app.py`:
```python
port = int(os.getenv("PORT", 8000))  # Change default port here
```

## API Endpoints

- `GET /` - Serves the chat interface
- `POST /api/chat` - Send a chat message
- `GET /api/health` - Health check endpoint
- `POST /api/clear` - Clear conversation history

## Troubleshooting

### API Key Issues

If you see "Gemini API key not configured":
1. Make sure you created a `.env` file (not just `.env.example`)
2. Check that your API key is correct
3. Verify the key is active at [Google AI Studio](https://makersuite.google.com/app/apikey)

### Port Already in Use

If port 8000 is already in use:
- Change the port in `.env` file: `PORT=8080`
- Or kill the process using port 8000

### Network Issues

If the API calls fail:
- Check your internet connection
- Verify the Gemini API is accessible from your network
- Check firewall settings

## Why Use This Instead of ChatGPT/Gemini Website?

1. **Bypass Network Blocks** - Works even when ChatGPT/Gemini websites are blocked
2. **Privacy** - Conversations stay on your local machine
3. **Customization** - Full control over the interface and behavior
4. **No Browser Extensions** - No need for VPNs or proxy extensions
5. **Offline Capable** - Interface works offline (API calls still need internet)

## Deploying to Vercel

This app can be deployed to Vercel for cloud hosting. See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed instructions.

### Quick Vercel Deployment Steps:

1. **Push your code to GitHub/GitLab/Bitbucket**
2. **Import project to Vercel** from your Git repository
3. **Add Environment Variable** in Vercel:
   - Go to Settings → Environment Variables
   - Add `GEMINI_API_KEY` with your API key value
   - Select all environments (Production, Preview, Development)
4. **Deploy** - Vercel will automatically build and deploy

**Important:** Make sure to add `GEMINI_API_KEY` in Vercel's environment variables, otherwise you'll get an error about the API key not being configured.

## Alternative API Options

While this project uses Gemini API, you can easily modify it to use:

- **OpenAI API** - Replace Gemini with GPT-3.5/GPT-4
- **Anthropic Claude API** - Use Claude models
- **Ollama** - Run models locally (completely offline)

## License

This project is open source and available for personal use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your API key is valid
3. Check the server logs for error messages

---

**Note:** This application requires an active internet connection to communicate with the Gemini API. The interface runs locally, but API calls go through Google's servers.

