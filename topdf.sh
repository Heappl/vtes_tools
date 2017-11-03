i=400
p=100
output=$1
shift
convert $* -density ${p}x${p} -units PixelsPerInch -resize $((i*192/100))x$((i*267/100)) -repage $((i*210/100))x$((i*297/100)) $output
