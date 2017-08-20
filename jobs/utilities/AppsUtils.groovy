package utilities

class AppsUtils {

    static defaultLogRotatorPolicy(job) {
        job.with {
            logRotator {
                daysToKeep(15)
                numToKeep(2)
            }
        }
    }

    static defaultWrappersPolicy(job) {
        job.with {
            wrappers {
                colorizeOutput()
                preBuildCleanup()
            }
        }
    }

//    Delete workspace at the end of the job (Success Unstable Failure Not-Built Aborted... Any case, the workspace is cleaned)
    static defaultPublishers(job) {
        job.with {
            publishers {
                wsCleanup()
            }
        }
    }


}