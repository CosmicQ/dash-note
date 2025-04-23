#terraform {
#  required_version = ">= 1.3.0"
#  backend "s3" {
#    bucket         = "my-terraform-state-bucket"
#    key            = "global/s3/terraform.tfstate"
#    region         = "us-west-2"
#    encrypt        = true
#    dynamodb_table = "terraform-state-lock"
#  }
#}
