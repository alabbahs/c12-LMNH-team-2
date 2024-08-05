resource "aws_lambda_function" "data_handling" {
  function_name = "c12-team2-etl-lambda"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "<your-account-id>.dkr.ecr.<region>.amazonaws.com/my-lambda-function:latest"  # Update this with your ECR image URI

  environment {
    variables = {
      RDS_ENDPOINT = aws_db_instance.rds_instance.endpoint
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
