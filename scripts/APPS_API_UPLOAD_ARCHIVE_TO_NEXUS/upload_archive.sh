#!/bin/bash
# On utilise set +x pour ne pas afficher les commandes sur la console
set +x
set -e
echo "####################################"
echo "=========== Debut Upload du fichier ======="
echo "####################################"

mv archiveFile ${archiveFile}
user="admin"
password="admin123"
if [ -z "${directory}" ]
then
    repo_url="http://192.168.1.97:9081/nexus/content/repositories/${repository}"
else
    repo_url="http://192.168.1.97:9081/nexus/content/repositories/${repository}/${target}"
fi
#--write-out "\nStatus: %{http_code}\n" \
curl -sSf -k -u ${user}:${password} -T ${archiveFile} ${repo_url}