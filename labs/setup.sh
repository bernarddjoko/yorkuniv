# pull the hadoop docker image

#check if the docker  group exists
#

if [ $(getent group admin) ]; then
    echo "group exists."
else
    echo "group does not exist."
    sudo groupadd docker
    sudo usermod -aG docker $USER
    fi






# docker pull sequenceiq/hadoop-docker:2.7.1
