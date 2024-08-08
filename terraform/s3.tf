provider "aws" {
  region = "eu-west-2"  # Specify your desired region
}

resource "aws_s3_bucket" "historical_data_bucket" {
  bucket = "my-historical-data-bucket"  # Use a unique bucket name

  tags = {
    Name        = "HistoricalDataBucket"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.historical_data_bucket.bucket

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
  bucket = aws_s3_bucket.historical_data_bucket.bucket

  rule {
    id     = "retain-for-30-days"
    status = "Enabled"

    filter {
      prefix = "historical/"
    }

    expiration {
      days = 30
    }
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.historical_data_bucket.bucket
}
