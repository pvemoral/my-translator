# My Translator

A text-to-podcast generation service that converts written content into audio podcast episodes using advanced text-to-speech technology and natural language processing.

## Overview

This Azure Function App provides an HTTP-triggered service that transforms text input into podcast-quality audio content. The service leverages Azure Cognitive Services for text-to-speech conversion and implements natural language processing for content optimization.

## Prerequisites

- **Azure Subscription**: Active Azure subscription with access to create resources
- **Azure CLI**: Version 2.30.0 or later
- **Azure Functions Core Tools**: Version 4.x
- **Python**: Version 3.8, 3.9, 3.10, or 3.11
- **pip**: Python package installer

## Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pvemoral/my-translator.git
   cd my-translator
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure local settings**:
   ```bash
   cp local.settings.json.example local.settings.json
   ```
   Edit `local.settings.json` with your Azure service keys and configuration.

5. **Run locally**:
   ```bash
   func start
   ```

## Azure Resources Required

### Core Services
- **Azure Function App**: Python 3.x runtime
- **Azure Storage Account**: For function app storage and audio file output
- **Azure Cognitive Services**: Speech service for text-to-speech conversion

### Optional Services
- **Azure Application Insights**: For monitoring and logging
- **Azure Key Vault**: For secure credential management

## Deployment Instructions

### Option 1: Deploy via Azure CLI

1. **Login to Azure**:
   ```bash
   az login
   ```

2. **Create Resource Group**:
   ```bash
   az group create --name my-translator-rg --location "East US"
   ```

3. **Create Storage Account**:
   ```bash
   az storage account create \
     --name mytranslatorstore \
     --resource-group my-translator-rg \
     --location "East US" \
     --sku Standard_LRS
   ```

4. **Create Function App**:
   ```bash
   az functionapp create \
     --resource-group my-translator-rg \
     --consumption-plan-location "East US" \
     --runtime python \
     --runtime-version 3.9 \
     --functions-version 4 \
     --name my-translator-app \
     --storage-account mytranslatorstore \
     --os-type Linux
   ```

5. **Deploy the function**:
   ```bash
   func azure functionapp publish my-translator-app
   ```

### Option 2: Deploy via VS Code

1. Install the **Azure Functions** extension
2. Sign in to your Azure account
3. Create new Function App in Azure
4. Deploy to Function App using the extension

### Option 3: Deploy via GitHub Actions

The repository includes a GitHub Actions workflow for automated deployment. Configure the following secrets in your repository:

- `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`: Download from Azure Portal
- `AZURE_FUNCTIONAPP_NAME`: Your function app name

## Environment Variables

Configure the following application settings in your Azure Function App:

```bash
# Required
SPEECH_SERVICE_KEY=your_cognitive_services_key
SPEECH_SERVICE_REGION=your_service_region
STORAGE_CONNECTION_STRING=your_storage_connection_string

# Optional
APPLICATION_INSIGHTS_KEY=your_app_insights_key
LOG_LEVEL=INFO
MAX_AUDIO_DURATION=1800  # 30 minutes
```

## API Usage

### Endpoint
```
POST https://your-function-app.azurewebsites.net/api/text-to-podcast
```

### Request Body
```json
{
  "text": "Your text content here",
  "voice": "en-US-AriaNeural",
  "speed": "medium",
  "format": "mp3"
}
```

### Response
```json
{
  "status": "success",
  "audio_url": "https://storage.../podcast.mp3",
  "duration": 120,
  "size": 2048576
}
```

## Monitoring and Troubleshooting

- **Logs**: View in Azure Portal > Function App > Monitor
- **Metrics**: Available in Application Insights
- **Local debugging**: Use `func start --verbose` for detailed logs

## Cost Optimization

- Use **Consumption Plan** for variable workloads
- Implement **function timeout** to prevent runaway costs
- Monitor **Cognitive Services** usage and set alerts
- Use **blob storage lifecycle** policies for audio file cleanup

## Security Considerations

- Store sensitive keys in **Azure Key Vault**
- Enable **HTTPS only** for the Function App
- Implement **IP restrictions** if needed
- Use **Managed Identity** for Azure service authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `func start`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
