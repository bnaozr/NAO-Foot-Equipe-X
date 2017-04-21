VnaoPath=`pwd`/
#export LD_LIBRARY_PATH=${VnaoPath}/naoqi/lib
PathToAdd=${VnaoPath}/naoqi/lib:${VnaoPath}V-REP_PRO_EDU_V3_3_2_64_Linux
if [ -z ${LD_LIBRARY_PATH+x} ]; 
then
    #echo "LD_LIBRARY_PATH is unset"
    export LD_LIBRARY_PATH=${PathToAdd}
else
    #echo "LD_LIBRARY_PATH is set to '$LD_LIBRARY_PATH'"
    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${PathToAdd}
fi
printenv | grep LD_LIBRARY_PATH
./V-REP_PRO_EDU_V3_3_2_64_Linux/vrepv1.sh &

