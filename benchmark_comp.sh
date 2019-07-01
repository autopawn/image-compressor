
rm output/*.bin || true
mkdir -p output

for img in $(find rgb8bit/ -type f | grep .ppm); do
    bname=$(basename "$img")
    target=output/"${bname%.ppm}".bin
    python3 compressor.py -c "$img" "$target"
done

for img in $(find rgb8bit/ -type f | grep .ppm); do
    bname=$(basename "$img")
    target=output/"${bname%.ppm}".png
    if [ ! -f "$target" ]; then
        optipng "$img" -out "$target"
    fi
done
