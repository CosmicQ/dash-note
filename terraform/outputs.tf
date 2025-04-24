
output "policy_arn" {
  value = aws_iam_policy.cloudwatch_dashboard_policy.arn
}

output "lambda_function_arn" {
  value = aws_lambda_function.dash_note.arn
}
