resource "azurerm_storage_account" "storage_account" {
  name = "hrstorage${random_integer.number.result}"
  account_tier = "Standard"
  location = var.location
  resource_group_name = azurerm_resource_group.storage_rg.name
  account_replication_type = "LRS"
}


resource "azurerm_storage_share" "upload_dbt" {
    name = "data"
    storage_account_name = azurerm_storage_account.storage_account.name
    quota = 100
}

resource "azurerm_storage_share_directory" "dbt_folder" {
    name = ".dbt"
    storage_share_id = azurerm_storage_share.upload_dbt.id
}

resource "azurerm_storage_share_file" "upload_dbt_profiles" {
    name = "profiles.yml"
    source = "assets/profiles.yml"
    storage_share_id = azurerm_storage_share.upload_dbt.id
    path = ".dbt"

    depends_on = [ azurerm_storage_share_directory.dbt_folder ]
  
}

