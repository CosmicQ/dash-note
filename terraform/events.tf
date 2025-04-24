
resource "aws_cloudwatch_event_rule" "dash_note_event_rule" {
  name          = "DashNoteEventRule"
  description   = "Routes DashboardNoteCreated events to the dash-note Lambda"
  event_pattern = jsonencode({
    source      = [ "com.my-api.dash-note" ]
    detail_type = [ "DashboardNoteCreated" ]
  })
}

resource "aws_lambda_permission" "allow_eventbridge_to_lambda" {
  statement_id  = "AllowEventBridgeInvocation"
  action        = "lambda:InvokeFunction"
  function_name = "dash-note"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.dash_note_event_rule.arn
}

resource "aws_cloudwatch_event_target" "dash_note_event_target" {
  rule          = aws_cloudwatch_event_rule.dash_note_event_rule.name
  target_id     = "dashNoteLambdaTarget"
  arn           = aws_lambda_function.dash_note.arn
}
