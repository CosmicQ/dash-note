
resource "aws_events_rule" "dash_note_event_rule" {
  name        = "DashNoteEventRule"
  description = "Routes DashboardNoteCreated events to the dash-note Lambda"
  event_pattern = jsonencode({
    source = [ "com.my-api.dash-note" ] #  Match the Source from your API Gateway integration
    detail_type = [ "DashboardNoteCreated" ] #  Match the DetailType
  })
}

resource "aws_lambda_permission" "allow_eventbridge_to_lambda" {
  statement_id  = "AllowEventBridgeInvocation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dash_note.name
  principal     = "events.amazonaws.com"
  source_arn    = aws_events_rule.dash_note_event_rule.arn
}

resource "aws_events_target" "dash_note_event_target" {
  rule      = aws_events_rule.dash_note_event_rule.name
  target_id = "dashNoteLambdaTarget" #  Unique target ID
  arn       = var.lambda_function_arn # Use the variable
}
