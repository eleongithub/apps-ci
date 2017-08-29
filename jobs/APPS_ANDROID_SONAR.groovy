import utilities.AppsUtils
// Job de contrôle de qualité pour l'application Android
def job = freeStyleJob('APPS_ANDROID_SONAR'){

    //    Définir le JDK par défaut

    // Description du job.
    description('Ce job permet de lancer un contrôle de qualité de code Sonar pour l\'application Android')


//    Définir les paramètres du Job
    parameters {
        stringParam('branch', 'master', 'Branche à utiliser pour le contrôle de code Sonar.')

    }

    //    Récupérer sur Git la branche à utiliser pour faire le deploiement
    scm {
        git {
            remote {
                url('https://github.com/eleongithub/MyApps.git')
            }
            branch('${branch}')
            extensions{
                localBranch('${branch}')
            }
        }
    }

    steps {
        gradle {
            tasks('clean sonarqube Dsonar.host.url=http://192.168.1.97:9000')
        }
    }
//    TODO Envoyer un mail de notification à la fin du deploiement
}
AppsUtils.defaultWrappersPolicy(job)
AppsUtils.defaultLogRotatorPolicy(job)