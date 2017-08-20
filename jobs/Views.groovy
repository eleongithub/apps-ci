listView('APPS_API_PROJECTS') {
// Adds columns to the views.
    columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()

// Sets a description for the view.
        description('APPS_API_PROJECTS')
// Adds jobs to the view.
        jobs {
            regex('APPS_API_.+')
        }
    }
}
