#!/bin/bash
# On utilise set +x pour ne pas afficher les commandes sur la console
set +x
set -e
echo "####################################"
echo "=========== Upload du fichier ======="
echo "####################################"

mv archiveFile ${archiveFile}
user="admin"
password="admin123"
# Vérifier si le paramètre directory a été renseigné.
if [ -z "${directory}" ]
then
    repo_url="http://192.168.0.10:9081/nexus/content/repositories/${repository}"
else
    repo_url="http://192.168.0.10:9081/nexus/content/repositories/${repository}/${target}"
fi
echo "URL Repositiory cible : $repo_url"
echo "nom du fichier archive à déposer : ${archiveFile}"
curl -v -u ${user}:${password} --upload-file ${archiveFile} ${repo_url}/${archiveFile}
echo "=========== Fin du dépôt du fichier ======="