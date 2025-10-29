resource "null_resource" "build_and_push_dashboard" {
  provisioner "local-exec" {
    command = <<EOT
      az acr login --name ${azurerm_container_registry.acr.name}
      docker buildx build --platform linux/amd64 \
        -f ../dockerfile.dashboard \
        -t ${azurerm_container_registry.acr.name}.azurecr.io/hr-project-dashboard:latest \
        ../ --push
    EOT
  }

  depends_on = [azurerm_container_registry.acr]
}

resource "azurerm_service_plan" "asp" {
    name                = "${var.prefix_app_name}-asp"
    location            = azurerm_resource_group.storage_rg.location
    resource_group_name = azurerm_resource_group.storage_rg.name
    os_type             = "Linux"
    sku_name            = "P0v3"

}

resource "azurerm_linux_web_app" "app" {
  name                = "${var.prefix_app_name}-app-${random_integer.number.result}"
  location            = azurerm_resource_group.storage_rg.location
  resource_group_name = azurerm_resource_group.storage_rg.name
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      docker_image_name   = "${azurerm_container_registry.acr.name}.azurecr.io/hr-project-dashboard:latest"
      docker_registry_url = "https://${azurerm_container_registry.acr.login_server}"
    }
  }

  storage_account {
    name         = "duckdbdata"
    type         = "AzureFiles"
    account_name = azurerm_storage_account.storage_account.name
    share_name   = azurerm_storage_share.upload_dbt.name
    access_key   = azurerm_storage_account.storage_account.primary_access_key
    mount_path   = "/mnt/data"
  }

  app_settings = {
    WEBSITES_PORT = "8501"
    DBT_PROFILES_DIR = "/mnt/data/.dbt"
    DUCKDB_PATH      = "/mnt/data/job_ads.duckdb"
  }

  depends_on = [
    null_resource.build_and_push_dashboard,
    azurerm_container_group.acg,
    azurerm_storage_share.upload_dbt]
}