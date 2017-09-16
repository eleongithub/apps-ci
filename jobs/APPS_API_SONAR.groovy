import utilities.AppsUtils
// Job d'exécution des tests Junit et transfert des résultats à Sonar
def job = mavenJob('APPS_API_SONAR_BRANCH'){

    // Définir le JDK par défaut

    // Description du job.
    description('Ce job permet de lancer un scan sonar sur une branche de  l\'API apps.')

//    Exécution automatique du job tous les jours à 6h et à 13H
    triggers {
        cron("H 6,13 * * *")
    }


//    Définir les paramètres du Job
    parameters {
        stringParam('branch', 'master', 'Branche à utiliser pour lancer un scan sonar')
//        TODO - à integrer liste dynamique des branches. Example : http://www.nachum234.com/automation/jenkins/dynamically-list-git-branches-in-jenkins-parameter/
//        TODO - https://jenkinsci.github.io/job-dsl-plugin/#method/javaposse.jobdsl.dsl.helpers.BuildParametersContext.activeChoiceReactiveParam
    }

//    Récupérer sur Git la branche à utiliser pour faire le snapshot
    scm {
        git {
            remote {
                url('https://github.com/eleongithub/apps-api.git')
            }
            branch('${branch}')
        }
    }

    goals('clean compile  install -Prun-its sonar:sonar -Dsonar.host.url=http://192.168.0.10:9000')
//    TODO Envoyer un mail de notification à la fin du build sonar
}
AppsUtils.defaultWrappersPolicy(job)
AppsUtils.defaultLogRotatorPolicy(job)
