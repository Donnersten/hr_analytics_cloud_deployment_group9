locals {
  # Parse the subscription id from env_variable.sh so runs don't require sourcing the file.
  env_file_content          = try(file("${path.module}/env_variable.sh"), "")
  subscription_line         = try(regex("ARM_SUBSCRIPTION_ID\\s*=\\s*\"[^\"]+\"", local.env_file_content), "")
  subscription_id_from_file = length(trimspace(local.subscription_line)) > 0 ? trimsuffix(trimprefix(trimspace(local.subscription_line), "ARM_SUBSCRIPTION_ID=\""), "\"") : null
}
