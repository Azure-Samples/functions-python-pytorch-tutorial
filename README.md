---
page_type: sample
languages:
- python
- html
products:
- azure-functions
description: "Predict ImageNet Classes with PyTorch and Azure Functions"
urlFragment: functions-python-pytorch-tutorial
---

# Make machine learning predictions with PyTorch and Azure Functions

## Run locally

Note, the instructions below assume you are using a Linux environment.

### Activate virtualenv 

1. `mkdir start`
1. `cd start`
1. `python -m venv .venv`
1. `source .venv/bin/activate`

### Initialize function app

1. `func init --worker-runtime python`
1. `func new --name classify --template "HTTP trigger"`

### Copy resources into the classify folder, assuming you run these commands from start

1. `cp ../resources/predict.py classify`
1. `cp ../resources/labels.txt classify`
1. Add the following dependencies to start/requirements.txt, installing some numerical libraries and PyTorch itself:

```bash
azure-functions
requests
numpy==1.15.4
https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp36-cp36m-win_amd64.whl; sys_platform == 'win32' and python_version == '3.6'
https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp36-cp36m-linux_x86_64.whl; sys_platform == 'linux' and python_version == '3.6'
https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp37-cp37m-win_amd64.whl; sys_platform == 'win32' and python_version == '3.7'
https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp37-cp37m-linux_x86_64.whl; sys_platform == 'linux' and python_version == '3.7'
https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp38-cp38-win_amd64.whl; sys_platform == 'win32' and python_version == '3.8'
https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp38-cp38-linux_x86_64.whl; sys_platform == 'linux' and python_version == '3.8'
torchvision==0.5.0
```
1. Install dependencies with `pip install --no-cache-dir -r requirements.txt`

### Update the function to run predictions

1. Add an `import` statement to `classify/__init__.py`

```{py}
import logging
import json
import azure.functions as func

from .predict import predict_image_from_url

```

1. Replace the entire contents of the `main` function with the following code:

```{py}
def main(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('img')
    logging.info('Image URL received: ' + image_url)

    results = predict_image_from_url(image_url)

    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    return func.HttpResponse(json.dumps(results), headers = headers)

```

### Run the local function

1. Run `func start` from within the start folder with the virtual environment activated.
1. Run `http://localhost:7071/api/classify?img=https://raw.githubusercontent.com/gvashishtha/functions-pytorch/master/resources/assets/Bernese-Mountain-Dog-Temperament-long.jpg`

### Create an Azure function
Run the following in the [Azure Cloud Shell](https://docs.microsoft.com/azure/cloud-shell/overview) to create a sample function app with a Python runtime:

```dotnetcli
#!/bin/bash

# Function app and storage account names must be unique.
storageName=mystorageaccount$RANDOM
functionAppName=myserverlessfunc$RANDOM
region=westeurope
pythonVersion=3.7

# Create a resource group.
az group create --name myResourceGroup --location $region

# Create an Azure storage account in the resource group.
az storage account create \
  --name $storageName \
  --location $region \
  --resource-group myResourceGroup \
  --sku Standard_LRS

# Create a serverless function app in the resource group.
az functionapp create \
  --name $functionAppName \
  --storage-account $storageName \
  --consumption-plan-location $region \
  --resource-group myResourceGroup \
  --os-type Linux \
  --runtime python \
  --runtime-version $pythonVersion \
  --functions-version 2
```

### Publish to Azure
1. `func azure functionapp publish <appname> --build local`
1. Test by using the suggested URL and appending `&img=https://raw.githubusercontent.com/gvashishtha/functions-pytorch/master/resources/assets/Bernese-Mountain-Dog-Temperament-long.jpg` at the end of the query string.

## License

See [LICENSE](LICENSE).

## Contributing

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
  
