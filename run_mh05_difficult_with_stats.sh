#!/bin/bash

# This script starts timing the MH05 difficult
# video file, while collecting stats of
# system level metrics and internal metrics
# of ORBSLAM3

# set up hooks to make sure regracefully exit
trap "echo 'The script is terminated'; kill -15 $(jobs -p); exit" SIGINT

# start timing with JTOP
python3 stats/collect_jtop_stats.py > jtop_stats.log &
jtop_pid=$!
echo "$jtop_pid is jtop"

# start perf
stats/kernel/kernel-jammy-src/tools/perf/perf record -e cache-misses -a &
perf_pid=$!
echo "$perf_pid is perf"

# move into orbslam for the final command
cd orb_slam3

# finally do the actual orbslam with sample video
./Examples/Stereo/stereo_euroc ./Vocabulary/ORBvoc.txt ./Examples/Stereo/EuRoC.yaml ~/Datasets/EuRoc/MH05 ./Examples/Stereo/EuRoC_TimeStamps/MH05.txt dataset-MH05_stereo 2>&1 | tee mh05_cout.log

# terminate the perf / jtop via SIGKILL
kill -15 $(jobs -p)
wait -n $jtop_pid
wait -n $perf_pid

# save results into results folder
echo 'saving results now'
cd && mkdir -p result_mh05
stats/kernel/kernel-jammy-src/tools/perf/perf script -i perf.data > perf_script_output.txt
mv perf.data perf_script_output.txt jtop_stats.log result_mh05/
mv orb_slam3/LocalMapTimeStats.txt orb_slam3/ExecMean.txt orb_slam3/f_dataset-MH05_stereo.txt orb_slam3/SessionInfo.txt orb_slam3/kf_dataset-MH05_stereo.txt orb_slam3/LBA_Stats.txt orb_slam3/TrackingTimeStats.txt orb_slam3/mh05_cout.log result_mh05/
chmod 777 result_mh05/perf.data
echo 'saved in result_mh05!'
