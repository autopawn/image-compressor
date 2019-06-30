
rm -rf output || true
mkdir -p output
for img in $(find rgb8bit/ -type f | grep .ppm); do
    bname=$(basename "$img")
    python3 compressor.py -c "$img" output/"${bname%.ppm}".bin
done
