set -ex

cd ../../ppe-backend && docker build . -t containers.cisco.com/cocreate/ppe-backend && cd -
cd ../../ppe-frontend && docker build . -t ppe-frontend && cd -
docker save containers.cisco.com/cocreate/ppe-backend -o ./ppe-backend.tar
docker save ppe-frontend -o ./ppe-frontend.tar
rm -rf release
mkdir release
cp ppe-backend.tar release/
cp ppe-frontend.tar release/
cp docker-compose.yml release/
cp verify.sh release/
cp nginx.conf release/
cp README.md release/
cp release-note.md release/
number=`date +'%Y-%m-%d'`
sed -e "s/\$date/$number/g" ./install_template.sh > ./install.sh
cp install.sh release/
tar zcvf ppe-release-$number.tar.gz -C release .
