provider "aws" {
  region = "us-west-2"  # Specify your desired AWS region
}

data "aws_iam_policy_document" "cloudwatch_dashboard_policy" {
  source_json_file = "${path.module}/policy.json"
}

resource "aws_iam_policy" "cloudwatch_dashboard_policy" {
  name        = "CloudWatchDashboardPolicy"
  description = "Policy to allow PutDashboard and GetDashboard actions on CloudWatch dashboards"
  policy      = data.aws_iam_policy_document.cloudwatch_dashboard_policy.json
}

resource "aws_iam_role" "dash_note_lambda_role" {
  name = "dash-note-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.dash_note_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "cloudwatch_dashboard_policy_attachment" {
  role       = aws_iam_role.dash_note_lambda_role.name
  policy_arn = aws_iam_policy.cloudwatch_dashboard_policy.arn
}

resource "aws_lambda_function" "dash_note" {
  filename         = "${path.module}/lambda_function.zip"
  function_name    = "dash-note"
  role             = aws_iam_role.dash_note_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("${path.module}/lambda_function.zip")
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

output "policy_arn" {
  value = aws_iam_policy.cloudwatch_dashboard_policy.arn
}

output "lambda_function_arn" {
  value = aws_lambda_function.dash_note.arn
}
