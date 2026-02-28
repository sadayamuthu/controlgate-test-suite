provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "vulnerable_bucket" {
  bucket = "my-public-company-data-bucket"
  
  # Vulnerability: Bucket is publicly readable
  acl    = "public-read"
}

resource "aws_security_group" "vulnerable_sg" {
  name        = "allow_all"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    # Vulnerability: Allowing ingress from 0.0.0.0/0
    cidr_blocks = ["0.0.0.0/0"]
  }
}
