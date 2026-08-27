variable "aws_region" {
  default = "ap-southeast-1"
}


variable "ubuntu_ami_id" {
  type = string
}

variable "ecr_repository_url" {
  type = string
}


variable "db_username" {
  type    = string
  default = "postgres"
}

variable "db_password" {
  type      = string
  sensitive = true
}