resource "azurerm_container_registry" "acr" {
    name = "hrprojectacr${random_integer.number.result}"
    location = var.location
    resource_group_name = azurerm_resource_group.storage_rg.name
    sku = "Basic"
    admin_enabled = true
}

resource "null_resource" "build_and_push_pipeline" {
  provisioner "local-exec" {
    command = <<EOT
      az acr login --name ${azurerm_container_registry.acr.name}
      docker buildx build --platform linux/amd64 \
        -f ../dockerfile.dwh \
        -t ${azurerm_container_registry.acr.name}.azurecr.io/hr-project-pipeline:latest \
        ../ --push
    EOT
  }

  depends_on = [azurerm_container_registry.acr]
}

resource "azurerm_container_group" "acg" {
  name                = "${var.prefix_app_name}-continst${random_integer.number.result}"
  location            = azurerm_resource_group.storage_rg.location
  resource_group_name = azurerm_resource_group.storage_rg.name
  ip_address_type     = "Public"
  dns_name_label      = "${var.prefix_app_name}-continst${random_integer.number.result}"
  os_type             = "Linux"

 depends_on = [
  null_resource.build_and_push_pipeline,
  azurerm_storage_share.upload_dbt
]

  image_registry_credential {
    server   = "${azurerm_container_registry.acr.name}.azurecr.io"
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }

  container {
    name   = "hr-pipeline"
    image  = "${azurerm_container_registry.acr.name}.azurecr.io/hr-project-pipeline:latest"
    cpu    = "1"
    memory = "4"

    ports {
      port     = 80
      protocol = "TCP"
    }

    ports {
      port     = 3000
      protocol = "TCP"
    }

    environment_variables = {
      DBT_PROFILES_DIR = "/mnt/data/.dbt"
      DUCKDB_PATH      = "/mnt/data/job_ads.duckdb"
    }

    volume {
      name       = "mnt"
      mount_path = "/mnt/data"
      read_only  = false
      share_name = azurerm_storage_share.upload_dbt.name

      storage_account_name = azurerm_storage_account.storage_account.name
      storage_account_key  = azurerm_storage_account.storage_account.primary_access_key
    }
  }
}