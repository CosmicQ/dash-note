data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "../src/dash_note.py"
  output_path = "${path.module}/dash_note.zip"
}

resource "aws_lambda_function" "dash_note" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "dash-note"
  description      = "dash-note creates vertical annotations on CloudWatch dashboards from EventBridge events"
  role             = aws_iam_role.dash_note_lambda_role.arn
  handler          = "dash_note.lambda_handler"
  runtime          = "python3.12"
  timeout          = 15
  source_code_hash = filebase64sha256(data.archive_file.lambda_zip.output_path)
}

