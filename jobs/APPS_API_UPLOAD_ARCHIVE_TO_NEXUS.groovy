import utilities.AppsUtils

// Job d'upload de fichiers sur le serveur Nexus
def job = freeStyleJob('APPS_API_UPLOAD_ARCHIVE_TO_NEXUS'){

    //    Définir le JDK par défaut

    // Description du job.
    description('Ce job permet d\'uploader des fichiers sur le serveur Nexus')


//    Définir les paramètres du Job
    parameters {
        booleanParam('debug', true, 'Exécuter le job en mode Debug.')
        choiceParam('repository', ['snapshots', 'releases'], 'Repository (Snapshots/Releases) sur lequel le fichier sera déposé.')
        stringParam('directory', '', 'Repertoire cible')
        fileParam('archiveFile', 'L\'archive à déposer sur le serveur Nexus.')
    }

    steps {
        shell(readFileFromWorkspace('scripts/APPS_API_UPLOAD_ARCHIVE_TO_NEXUS/upload_archive.sh'))
    }
}
AppsUtils.defaultWrappersPolicy(job)
AppsUtils.defaultLogRotatorPolicy(job)

