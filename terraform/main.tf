data "local_file" "cloudwatch_dashboard_policy" {
  filename = "../files/policy.json"
}

resource "aws_iam_policy" "cloudwatch_dashboard_policy" {
  name        = "CloudWatchDashboardPolicy"
  description = "Policy to allow PutDashboard and GetDashboard actions on CloudWatch dashboards"
  policy      = data.local_file.cloudwatch_dashboard_policy.content
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


