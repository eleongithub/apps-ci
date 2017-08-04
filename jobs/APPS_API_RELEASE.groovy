import utilities.DbUtils

// Inspirer en partie de ce lien http://www.baeldung.com/maven-release-nexus
// Job de création d'une version de release stable de l'application et upload des livrables sur le repository Nexus
def job = mavenJob('APPS_API_RELEASE'){

    //    Définir le JDK par défaut

    // Description du job.
    description('Ce job permet de créer une version release stable de l\'application doctolib')


//    Définir les paramètres du Job
    parameters {
//        TODO - à integrer liste dynamique des branches. Example : http://www.nachum234.com/automation/jenkins/dynamically-list-git-branches-in-jenkins-parameter/
//        TODO - https://jenkinsci.github.io/job-dsl-plugin/#method/javaposse.jobdsl.dsl.helpers.BuildParametersContext.activeChoiceReactiveParam
        stringParam('branch', 'master', 'Branche à utiliser pour effectuer la release')
        stringParam('releaseVersion', '', 'Version de release à produire.')
        stringParam('developmentVersion', '', 'Version de developpement à initialiser après le release')
    }

//    Récupérer sur Git la branche à utiliser pour faire le snapshot
    scm {
        git {
            remote {
                url('https://github.com/eleongithub/doctolib.git')
            }
            branch('${branch}')
            extensions{
                localBranch('${branch}')
            }
        }
    }
//    Liste des goals pour réaliser la release
    goals('release:clean release:prepare release:perform clean -Darguments="-DskipTests"')
    mavenInstallation('Maven 3.3.9')
//    TODO Envoyer un mail de notification à la fin du release
}
DbUtils.defaultWrappersPolicy(job)
DbUtils.defaultLogRotatorPolicy(job)
