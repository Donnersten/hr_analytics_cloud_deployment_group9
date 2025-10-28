terraform {
  required_providers {
    azurerm = {
        source = "hashicorp/azurerm"
        version = "~>4.3"
    }
  }
    required_version = "~> 1.13.0"
}

provider "azurerm" {
    features {

    }
    subscription_id = "b85e9682-f16d-42df-9da5-73b87d659d28"
}

