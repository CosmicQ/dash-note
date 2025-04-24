# dash_note
This is a serverless app that creates vertical annotations on a cloudformation dashboard.

To send an event to the app, you will need to have these parameters:


CLI
```
aws events put-events --entries '[{"Source": "com.example.my-dashboard-app", "DetailType": "DashboardUpdated", "Detail": "{\"dashboardName\": \"My Performance Dashboard\", \"note\": \"Significant increase in user engagement metrics this week.\"}"}]'

```

