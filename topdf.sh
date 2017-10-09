i=1000
convert $* -density ${i}x${i} -units PixelsPerInch -resize $((i*192/100))x$((i*267/100)) -repage $((i*210/100))x$((i*297/100)) cards.pdf
