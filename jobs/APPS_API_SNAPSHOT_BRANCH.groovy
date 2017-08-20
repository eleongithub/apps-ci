import utilities.AppsUtils
// Job de déploiement d'une version snapshots de l'application sur le repository Nexus
def job = mavenJob('APPS_API_SNAPSHOT_BRANCH'){

    //    Définir le JDK par défaut

    // Description du job.
    description('Ce job permet de lancer un snapshot de l\'API apps')


//    Définir les paramètres du Job
    parameters {
        stringParam('branch', 'master', 'Branche à utiliser pour effectuer le snapshot')
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

    goals('clean deploy -DskipTests')
//    TODO Envoyer un mail de notification à la fin du snapshot
}
AppsUtils.defaultWrappersPolicy(job)
AppsUtils.defaultLogRotatorPolicy(job)
