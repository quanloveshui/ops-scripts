#!/bin/bash



#检查执行脚本的user，必须root or sudo 执行
function check_user(){
    user=$(env | grep 'USER' |grep -v 'SUDO' |grep -v 'USERNAME'|  cut -d "=" -f 2)
    if [ "$user" != "root" ]
    then
        echo "Current user is not ROOT.Please run as Root user."
        exit 1
    else
        echo "continue"
    fi
}


#确认是否升级
function check_upgrade(){
    read -p "请确认是否升级GSLB应用(yes|no)：" choose
    if [ $choose = "yes" ]
    then
        echo  '将升级GSLB应用'
        sleep 1

    elif [ $choose = "no" ]
    then
        echo  '选择不升级GSLB应用,将退出升级程序'
        exit 1

    else
        echo '选择错误,将退出升级程序'
        exit 1
    fi

}

check_user
check_upgrade


gslb_dir=/usr/local/apache-tomcat-6.0.53/webapps
tar_dir=/opt/upgrade
tomcat_dir=/usr/local/apache-tomcat-6.0.53

if [ -d $tomcat_dir ]
then
    # stop tomcat
    cd $tomcat_dir/bin
    ./shutdown.sh
    kill -9 $(pgrep java)
else
    echo "tomcat path does no exist"
    exit 1
fi


echo "backup gslb and upgrade"
sleep 1

rm -rf $gslb_dir/gslb-bak.tar.gz
cd $gslb_dir
tar -zcvf gslb-bak.tar.gz gslb
if [ $? == 0 ]
then
    rm -rf $gslb_dir/gslb
    cp $tar_dir/gslb.tar.gz $gslb_dir
    tar -zxvf $gslb_dir/gslb.tar.gz -C $gslb_dir
    rm -rf $gslb_dir/gslb.tar.gz
    cp $tar_dir/jdbc.properties $gslb_dir/gslb/WEB-INF/classes/jdbc.properties 
    cp $tar_dir/bme.properties $gslb_dir/gslb/WEB-INF/classes/bme.properties
    echo "start gslb"
    sleep 1
    cd $tomcat_dir/bin
    ./startup.sh
else
    echo "backup gslb fail"
    exit 1
fi
